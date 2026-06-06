import os
import sys
import pickle
import numpy as np
import faiss
from fastembed import TextEmbedding
from rag.llm import generate_answer

# Reconfigure stdout to use UTF-8 to prevent Windows terminal emoji encoding errors
sys.stdout.reconfigure(encoding='utf-8')

# Setup paths relative to this script's location
RAG_DIR = os.path.dirname(os.path.abspath(__file__))
faiss_index_path = os.path.join(RAG_DIR, "faiss_index.bin")
texts_pkl_path = os.path.join(RAG_DIR, "texts.pkl")

# Load index + texts
if not os.path.exists(faiss_index_path) or not os.path.exists(texts_pkl_path):
    print("⚠️ Warning: FAISS index or texts pickle not found. Run ingest.py first!")
    index = None
    texts = []
else:
    index = faiss.read_index(faiss_index_path)
    with open(texts_pkl_path, "rb") as f:
        texts = pickle.load(f)

# Load embedding model using FastEmbed for CPU-efficient, low-memory execution
model = TextEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")


def retrieve(query, k=6):
    if index is None or not texts:
        return []
    try:
        query_embedding = np.array(list(model.embed([query]))).astype("float32")
        D, I = index.search(query_embedding, k)

        results = []
        for i in I[0]:
            if i < len(texts):
                results.append(texts[i])  # This is a dict: {"text": "...", "source": "...", "page": ...}

        return results

    except Exception as e:
        print("❌ Error in retrieval:", e)
        return []


def ask(query):
    chunks = retrieve(query)

    if not chunks:
        return "No relevant legal information found.", []

    # Format context for the LLM with metadata citations
    context_parts = []
    for i, chunk in enumerate(chunks):
        context_parts.append(
            f"[Document {i+1}]: {chunk['source']} (Page {chunk['page']})\n"
            f"Content: {chunk['text']}"
        )
    context = "\n\n---\n\n".join(context_parts)

    answer = generate_answer(context, query)

    # Extract unique source filenames and page numbers
    sources = []
    seen = set()
    for chunk in chunks:
        source_key = (chunk["source"], chunk["page"])
        if source_key not in seen:
            seen.add(source_key)
            sources.append({
                "file": chunk["source"],
                "page": chunk["page"]
            })

    return answer, sources


if __name__ == "__main__":
    while True:
        query = input("\nAsk your legal question (type 'exit' to quit): ")

        if query.lower() == "exit":
            break

        answer, sources = ask(query)

        print("\n🤖 Answer:\n")
        print(answer)
        
        if sources:
            print("\n📚 Sources:")
            for s in sources:
                print(f"- {s['file']} (Page {s['page']})")
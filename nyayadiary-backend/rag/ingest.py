import os
import sys
import pickle
import numpy as np
import faiss
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer

# Reconfigure stdout to use UTF-8 to prevent Windows terminal emoji encoding errors
sys.stdout.reconfigure(encoding='utf-8')

# Setup paths relative to this script's location
RAG_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.dirname(RAG_DIR)
DATA_DIR = os.path.join(BACKEND_DIR, "data")

faiss_index_path = os.path.join(RAG_DIR, "faiss_index.bin")
texts_pkl_path = os.path.join(RAG_DIR, "texts.pkl")

print("🚀 Starting ingestion...")
print(f"📂 Scanning data directory: {DATA_DIR}")

if not os.path.exists(DATA_DIR):
    print(f"❌ Data directory not found: {DATA_DIR}")
    os.makedirs(DATA_DIR)
    print("📁 Created empty data directory. Please add PDF files to it.")
    exit()

# Find all PDF files in the data directory
pdf_files = [f for f in os.listdir(DATA_DIR) if f.lower().endswith(".pdf")]

if not pdf_files:
    print("❌ No PDF files found in the data directory!")
    exit()

print(f"📚 Found {len(pdf_files)} PDF file(s): {', '.join(pdf_files)}")

all_documents = []
for pdf in pdf_files:
    pdf_path = os.path.join(DATA_DIR, pdf)
    print(f"📄 Loading {pdf}...")
    try:
        loader = PyPDFLoader(pdf_path)
        docs = loader.load()
        all_documents.extend(docs)
        print(f"✅ Loaded {len(docs)} pages from {pdf}")
    except Exception as e:
        print(f"❌ Error loading {pdf}: {e}")

if not all_documents:
    print("❌ No pages could be loaded from any PDF files.")
    exit()

print(f"✂️ Splitting {len(all_documents)} pages into chunks...")
splitter = RecursiveCharacterTextSplitter(
    chunk_size=400,
    chunk_overlap=50
)
docs = splitter.split_documents(all_documents)
print(f"✅ Created {len(docs)} chunks")

print("🧠 Loading embedding model...")
model = SentenceTransformer("all-MiniLM-L6-v2")

# Store both text content and source metadata
texts_data = []
for doc in docs:
    file_path = doc.metadata.get("source", "Unknown Document")
    filename = os.path.basename(file_path)
    page_num = doc.metadata.get("page", 0) + 1  # 1-indexed page
    texts_data.append({
        "text": doc.page_content,
        "source": filename,
        "page": page_num
    })

texts_to_embed = [item["text"] for item in texts_data]

print("⚡ Generating embeddings...")
embeddings = model.encode(texts_to_embed, show_progress_bar=True)

# convert to float32 for FAISS
embeddings = np.array(embeddings).astype("float32")

print("📦 Creating FAISS index...")
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

print("💾 Saving files...")
faiss.write_index(index, faiss_index_path)

with open(texts_pkl_path, "wb") as f:
    pickle.dump(texts_data, f)

print(f"✅ DONE: FAISS index saved to {faiss_index_path}")
print(f"✅ DONE: Metadata + text chunks saved to {texts_pkl_path}")
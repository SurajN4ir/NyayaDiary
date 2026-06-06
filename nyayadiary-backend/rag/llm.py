from groq import Groq
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("❌ GROQ_API_KEY not found. Check your .env file.")

client = Groq(api_key=GROQ_API_KEY)


def generate_answer(context, query):
    prompt = f"""
You are NyayaDiary, a legal awareness assistant for Indian citizens.

Your task:
- Explain laws clearly and correctly
- Use ONLY the context provided
- If context is partial, still answer as best as possible using it
- Do NOT say "constitution does not list rights" if information is present
- Summarize clearly in bullet points if needed

Context:
{context}

Question:
{query}

Answer clearly:
Give a complete answer. If it's a list, list all key points.
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are a helpful legal assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=500
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        print(" Please Check,LLM Error:", e)
        return "Something went wrong while generating the answer."
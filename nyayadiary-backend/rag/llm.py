from groq import Groq
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("❌ GROQ_API_KEY not found. Check your .env file.")

client = Groq(api_key=GROQ_API_KEY)


def generate_answer(context, query, history=None):
    messages = [
        {
            "role": "system",
            "content": "You are NyayaDiary, a helpful legal assistant for Indian citizens. Explain laws clearly using the provided context."
        }
    ]

    if history:
        # Pass the last 5 messages to maintain conversation flow
        for msg in history[-5:]:
            role = "user" if getattr(msg, "sender", None) == "user" or msg.get("sender", None) == "user" else "assistant"
            text = getattr(msg, "text", "") or msg.get("text", "")
            messages.append({"role": role, "content": text})

    prompt = f"""
You are NyayaDiary, an empathetic and highly structured legal awareness assistant for Indian citizens.
Your task is to analyze the user's question and the provided context, and give a highly practical, structured response.

Strict Output Structure:
1. **⚖️ Legal Analysis**: Explain what the law says about the user's situation in simple, easy-to-understand language. Cite specific sections from the Context (e.g. BNS, CrPC, etc.).
2. **📋 Action Plan (Do This, Do That)**: Provide a concrete, step-by-step checklist of what the user should practically do next in the real world (e.g., "Step 1: Document all threat messages...", "Step 2: File a police complaint...", "Step 3: Consult a civil lawyer...").
3. **⚠️ Disclaimer**: A standard brief disclaimer stating that this is for educational purposes and not formal legal advice.

Context:
{context}

Question:
{query}

Generate the response following this strict format (using bold section headers):
"""
    messages.append({"role": "user", "content": prompt})

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=messages,
            temperature=0.2,
            max_tokens=500
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        print(" Please Check,LLM Error:", e)
        return "Something went wrong while generating the answer."
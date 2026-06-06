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
You are NyayaDiary, a legal awareness assistant for Indian citizens.

Your task:
- Explain laws clearly and correctly using the provided Context.
- Summarize clearly in bullet points if needed.

Context:
{context}

Question:
{query}

Answer clearly and directly:
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
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from typing import List, Optional

from rag.query import ask

app = FastAPI()

# 🔥 allow frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatMessage(BaseModel):
    sender: str
    text: str

class Query(BaseModel):
    query: str
    history: Optional[List[ChatMessage]] = []

@app.get("/")
def home():
    return {"message": "NyayaDiary backend running 🚀"}

@app.post("/chat")
def chat(q: Query):
    answer, sources = ask(q.query, q.history)
    return {"response": answer, "sources": sources}
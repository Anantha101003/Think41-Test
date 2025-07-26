from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import get_db, create_tables
from models import ConversationSession, ConversationMessage, User
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

app = FastAPI()

# Allow CORS for local frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    create_tables()

class ChatRequest(BaseModel):
    user_id: str
    message: str
    conversation_id: Optional[int] = None

class ChatResponse(BaseModel):
    conversation_id: int
    messages: List[dict]

@app.post("/api/chat", response_model=ChatResponse)
def chat_endpoint(payload: ChatRequest, db: Session = Depends(get_db)):
    # Find or create conversation session
    if payload.conversation_id:
        session = db.query(ConversationSession).filter_by(id=payload.conversation_id).first()
        if not session:
            raise HTTPException(status_code=404, detail="Conversation not found")
    else:
        session = ConversationSession(user_id=payload.user_id)
        db.add(session)
        db.commit()
        db.refresh(session)

    # Store user message
    user_msg = ConversationMessage(
        session_id=session.id,
        role="user",
        content=payload.message,
        timestamp=datetime.utcnow()
    )
    db.add(user_msg)
    db.commit()

    # Integrate Groq LLM for AI response
    import os
    from groq import Groq
    from dotenv import load_dotenv
    load_dotenv()
    
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    if not GROQ_API_KEY:
        raise HTTPException(status_code=500, detail="Groq API key not set")

    # Gather conversation history for context
    messages = db.query(ConversationMessage).filter_by(session_id=session.id).order_by(ConversationMessage.timestamp).all()
    chat_history = [
        {"role": m.role, "content": m.content} for m in messages
    ]
    chat_history.append({"role": "user", "content": payload.message})

    # Clarifying question logic (simple example)
    def needs_clarification(message):
        keywords = ["order", "product", "return", "status", "inventory"]
        return not any(k in message.lower() for k in keywords)

    if needs_clarification(payload.message):
        ai_content = "Could you please clarify your request regarding our e-commerce services?"
    else:
        # Call Groq LLM
        client = Groq(api_key=GROQ_API_KEY)
        try:
            response = client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[{"role": m["role"], "content": m["content"]} for m in chat_history],
                max_tokens=256,
                temperature=0.7,
            )
            ai_content = response.choices[0].message.content
        except Exception as e:
            ai_content = f"[LLM error: {str(e)}]"

    ai_msg = ConversationMessage(
        session_id=session.id,
        role="ai",
        content=ai_content,
        timestamp=datetime.utcnow()
    )
    db.add(ai_msg)
    db.commit()

    # Return all messages in this session
    messages = db.query(ConversationMessage).filter_by(session_id=session.id).order_by(ConversationMessage.timestamp).all()
    messages_out = [
        {"role": m.role, "content": m.content, "timestamp": m.timestamp.isoformat()} for m in messages
    ]
    return ChatResponse(conversation_id=session.id, messages=messages_out)

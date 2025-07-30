from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import get_db, create_tables
from models import ConversationSession, ConversationMessage, User
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

app = FastAPI()

from fastapi import Query

# --- Conversation session/history endpoints ---
@app.get("/api/sessions")
def get_sessions(user_id: str = Query(...), db: Session = Depends(get_db)):
    sessions = db.query(ConversationSession).filter_by(user_id=user_id).order_by(ConversationSession.created_at.desc()).all()
    return {
        "sessions": [
            {
                "conversation_id": s.id,
                "created_at": s.created_at.isoformat(),
                "updated_at": s.updated_at.isoformat(),
            }
            for s in sessions
        ]
    }

@app.get("/api/session/{session_id}")
def get_session(session_id: int, db: Session = Depends(get_db)):
    session = db.query(ConversationSession).filter_by(id=session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    messages = db.query(ConversationMessage).filter_by(session_id=session_id).order_by(ConversationMessage.timestamp).all()
    return {
        "conversation_id": session.id,
        "messages": [
            {
                "role": m.role,
                "content": m.content,
                "timestamp": m.timestamp.isoformat(),
            }
            for m in messages
        ],
    }

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
        {"role": "assistant" if m.role == "ai" else m.role, "content": m.content} for m in messages
    ]
    chat_history.append({"role": "user", "content": payload.message})

    # Clarifying question logic (simple example)
    def needs_clarification(message):
        keywords = ["order", "product", "return", "status", "inventory"]
        return not any(k in message.lower() for k in keywords)

    if needs_clarification(payload.message):
        ai_content = "Could you please clarify your request regarding our e-commerce services?"
    else:
        # --- Product lookup and context enrichment for demo ---
        import re
        from models import Product
        product_keywords = ["shirt","cap","hat","swimsuit","bikini","shorts","jacket","jeans","pant","dress","skirt","top","t-shirt","blouse","sweater","hoodie","coat","scarf","sock","shoe","sandal","boot","glove","belt","bag","purse","wallet","watch","suit","blazer","vest","tie"]
        user_msg = payload.message.lower()
        found = None
        for kw in product_keywords:
            if kw in user_msg:
                found = kw
                break
        color_match = re.search(r"(red|blue|black|white|navy|khaki|olive|plaid|camo|solid|print|stripe|grey|gray|beige|brown|orange|gold|silver|ivory|maroon|teal|aqua|coral|mint|peach|lime|mustard|burgundy|charcoal|denim|tan|turquoise|magenta|cream|off[- ]white|multicolor|violet|indigo|bronze|rose|wine|cherry|lemon|emerald|sapphire|ruby|pearl|copper|blush|fuchsia|mauve|taupe|camel|sand|rust|slate|peacock|eggplant|orchid|mocha|espresso|latte|cobalt|sky|seafoam|forest|pine|sage|spruce|mint|apple|melon|berry|stone|ash|cloud|smoke|storm|shadow|dove|graphite|midnight|ocean|ice|frost|snow)", user_msg, re.IGNORECASE)
        color = color_match.group(1) if color_match else None
        products = []
        if found:
            query = db.query(Product)
            if color:
                query = query.filter(Product.name.ilike(f"%{color}%"))
            query = query.filter(Product.name.ilike(f"%{found}%"))
            products = query.limit(3).all()
        # Build product context for LLM
        product_context = ""
        if products:
            product_context = "Available products matching your request:\n"
            for p in products:
                product_context += f"- {p.name} (Category: {p.category}, Brand: {p.brand}, Price: ${p.retail_price})\n"
        # Add product context as system prompt if any
        llm_messages = chat_history.copy()
        if product_context:
            llm_messages.insert(0, {"role": "system", "content": product_context})
        # Call Groq LLM
        client = Groq(api_key=GROQ_API_KEY)
        try:
            response = client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[{"role": m["role"], "content": m["content"]} for m in llm_messages],
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

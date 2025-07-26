# Customer Support Chatbot for E-commerce Clothing Site

This project implements a conversational AI chatbot for an e-commerce clothing site that can answer customer queries about products, orders, and inventory.

## Project Structure

```
├── backend/     # Backend service with API endpoints and database
├── frontend/    # Frontend UI for the chatbot interface
├── data/        # E-commerce CSV dataset files
└── README.md    # This file
```

## Features

The chatbot can handle queries like:
- "What are the top 5 most sold products?"
- "Show me the status of order ID 12345."
- "How many Classic T-Shirts are left in stock?"

## Milestone Progress

- [x] Milestone 1: Environment Setup
- [x] Milestone 2: Database Setup and Data Ingestion
- [x] Milestone 3: Data Schemas
- [x] Milestone 4: Core Chat API
- [x] Milestone 5: LLM Integration and Business Logic
- [x] Milestone 6: Frontend Implementation

## Tech Stack

- Backend: FastAPI (Python)
- Database: SQLite (default) or PostgreSQL (optional)
- LLM: Groq API
- Frontend: React (PWA)

## Getting Started

### 1. Backend Setup

```sh
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
# Add your Groq API key to .env:
echo GROQ_API_KEY=your_groq_api_key > .env
# (Optional) Edit DATABASE_URL in .env for PostgreSQL
python load_data.py  # Ingest e-commerce CSV data
uvicorn main:app --reload
```

### 2. Frontend Setup

```sh
cd frontend
npm install
npm start
```
Visit [http://localhost:3000](http://localhost:3000)

### 3. API Usage
- POST `/api/chat` with `{ user_id, message, conversation_id? }`
- Returns conversation history with LLM-powered responses

## Project Completion
All milestones are complete. The app supports multi-user, multi-session chat, LLM integration, and a modern React frontend.

---

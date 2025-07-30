# E-Commerce Chatbot: Full-Stack Demo Guide

A production-ready, conversational AI chatbot for e-commerce clothing sites. This project demonstrates:
- Real-time product lookup and order queries using LLM (Groq)
- FastAPI backend with SQLAlchemy and PostgreSQL
- React frontend with modern chat UI and session history
- Dockerized deployment for easy demo and production

---

## 1. Architecture Overview

```
project-root/
├── backend/      # FastAPI backend, SQLAlchemy models, Groq LLM integration
├── frontend/     # React app, Context API, chat UI, Nginx proxy
├── data/         # E-commerce CSVs (products, orders, users, etc.)
├── docker-compose.yml
├── .env          # Secrets (GROQ_API_KEY, DB config)
└── README.md     # This guide
```

- **Backend:** FastAPI, SQLAlchemy ORM, Groq LLM API
- **Database:** PostgreSQL (default via Docker) or SQLite (dev)
- **Frontend:** React (Context API for chat state), Nginx for API proxy
- **LLM:** Groq API (Llama 3), prompt enrichment with real product data

---

## 2. Key Features

- Natural language chat about products, orders, and inventory
- Real product lookup: chatbot injects live product info into LLM prompt
- Multi-session, multi-user conversation history
- Modern UI: chat window, sidebar for past sessions
- Docker Compose for one-command deployment
- Secure: API keys in .env, not in code

---

## 3. How the Chatbot Works

### Backend Logic
- User sends a message (e.g., "Show me red shirts")
- Backend parses for product type (e.g., shirt) and color (e.g., red)
- Queries the Product table for up to 3 best matches
- Injects product details as a `system` prompt for the LLM
- LLM (Groq) responds with contextually accurate info about actual inventory
- All messages and sessions are persisted in the database

### Example LLM Prompt Enrichment
```
System prompt:
Available products matching your request:
- Red Classic Shirt (Category: Shirts, Brand: Levi's, Price: $29.99)
- Red Polo Shirt (Category: Shirts, Brand: Polo, Price: $39.99)
...
```

---

## 4. Getting Started: Dockerized Demo (Recommended)

### Prerequisites
- [Docker](https://www.docker.com/get-started) and [Docker Compose](https://docs.docker.com/compose/)
- Groq API key ([get yours](https://console.groq.com/))

### Quickstart
```sh
# 1. Clone the repo and cd into project root
# 2. Add your Groq API key to .env at the root:
echo GROQ_API_KEY=your_groq_api_key > .env
# 3. Start all services
docker-compose up --build
# 4. (First time only) Ingest demo data:
docker-compose exec backend python load_data.py
```
- Backend: http://localhost:8000
- Frontend: http://localhost:3000

---

## 5. Manual Local Setup (Advanced)

### Backend
```sh
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
echo GROQ_API_KEY=your_groq_api_key > .env
# (Optional) Edit DATABASE_URL in .env for PostgreSQL
python load_data.py  # Ingest CSV data
uvicorn main:app --reload
```

### Frontend
```sh
cd frontend
npm install
npm start
```
Go to http://localhost:3000

---

## 6. API Reference

### POST `/api/chat`
Request:
```json
{
  "user_id": "demo_user",
  "message": "Show me blue jeans",
  "conversation_id": "..." // optional
}
```
Response: Full conversation history (including LLM and user messages)

### GET `/api/sessions`
- Returns all conversation sessions for the user

### GET `/api/session/{id}`
- Returns all messages for a given session

---

## 7. Product Lookup & LLM Context Logic
- Backend parses user message for product keywords and colors
- Queries Product table for matches (name, color)
- Top 3 results injected as a system prompt before LLM call
- LLM response is grounded in real, current inventory
- If no match, LLM responds normally

---

## 8. Demo & Troubleshooting Tips
- For best demo, ask: "Do you have red shirts?" or "Show me blue jeans"
- Data is resettable: re-run `load_data.py` to reload demo data
- If chat UI doesn't work:
  - Check Docker Compose logs (`docker-compose logs`)
  - Ensure .env has valid GROQ_API_KEY
  - Make sure frontend uses relative API URLs (not hardcoded localhost)
  - Try restarting containers: `docker-compose restart`
- For CORS/API errors: Nginx proxy in frontend container handles routing

---

## 9. Security & Secrets
- Never commit `.env` with secrets to version control
- All API keys and DB credentials are loaded from environment at runtime

---

## 10. Project Completion & Customization
- All major milestones complete: DB, backend, LLM, frontend, Docker
- Easy to extend: add more product attributes, new LLMs, or custom business logic
- For production, review Docker security and environment variable handling

---

## 11. Credits
- Built by [Your Team/Name]
- Powered by Groq, FastAPI, React, PostgreSQL

---

For questions or further customization, see code comments or contact the maintainer.

### 1. Environment Setup
- Project structure created for backend (FastAPI), frontend (React), and data ingestion.
- Python virtual environment and Node.js project initialized.
- `.gitignore` and `.env` files set up for security and best practices.

### 2. Database Setup and Data Ingestion
- SQLAlchemy models defined for e-commerce entities: DistributionCenter, Product, User, Order, OrderItem, InventoryItem.
- Data ingestion script (`load_data.py`) loads CSV datasets into the database.
- Supports SQLite by default; PostgreSQL available via Docker Compose (`backend/docker-compose.yml`).
- To use PostgreSQL, run:
  ```sh
  cd backend
  docker-compose up -d
  # Set DATABASE_URL in .env to:
  # postgresql://postgres:password@localhost:5432/ecommerce_chatbot
  ```

### 3. Data Schemas
- Database schemas for all e-commerce entities and conversation history.
- ConversationSession and ConversationMessage models support multi-user, multi-session chat.

### 4. Core Chat API
- FastAPI backend exposes `/api/chat` endpoint.
- Accepts user messages, persists them, and returns full conversation history.
- API supports multi-session, multi-user chat.

### 5. LLM Integration and Business Logic
- Integrates Groq LLM API for AI-powered responses.
- Stores Groq API key securely in `.env`.
- Implements clarifying question logic if user input is ambiguous.
- Placeholder for business logic to query e-commerce data and provide smart responses.

### 6. Frontend Implementation
- React app (PWA) created for chat UI.
- Connects to backend `/api/chat` endpoint.
- Core chat window, message display, user input, and session persistence.

### 7. Client-side State Management
- Uses React Context API to manage message list, loading status, and user input value.
- Centralizes state for scalability and maintainability.

### 8. Conversation History Panel
- Modern sidebar UI displays all past user sessions.
- Users can click a session to load its full chat history instantly.
- Fully integrated with backend session APIs.

### 9. Full-Stack Integration
- React frontend connects to FastAPI backend via `/api/chat` and related endpoints.
- CORS configured for seamless cross-origin requests.
- All chat and conversation history features work end-to-end, including multi-session support.

### 10. Dockerization
- Dockerfile for backend (FastAPI + Uvicorn).
- Dockerfile for frontend (React production build served by Nginx).
- Unified `docker-compose.yml` orchestrates the database, backend, and frontend.
- One command (`docker-compose up --build`) starts the entire stack for production or demo.

### 1. Environment Setup
- Project structure created for backend (FastAPI), frontend (React), and data ingestion.
- Python virtual environment and Node.js project initialized.
- `.gitignore` and `.env` files set up for security and best practices.

### 2. Database Setup and Data Ingestion
- SQLAlchemy models defined for e-commerce entities: DistributionCenter, Product, User, Order, OrderItem, InventoryItem.
- Data ingestion script (`load_data.py`) loads CSV datasets into the database.
- Supports SQLite by default; PostgreSQL available via Docker Compose (`backend/docker-compose.yml`).
- To use PostgreSQL, run:
  ```sh
  cd backend
  docker-compose up -d
  # Set DATABASE_URL in .env to:
  # postgresql://postgres:password@localhost:5432/ecommerce_chatbot
  ```

### 3. Data Schemas
- Database schemas for all e-commerce entities and conversation history.
- ConversationSession and ConversationMessage models support multi-user, multi-session chat.

### 4. Core Chat API
- FastAPI backend exposes `/api/chat` endpoint.
- Accepts user messages, persists them, and returns full conversation history.
- API supports multi-session, multi-user chat.

### 5. LLM Integration and Business Logic
- Integrates Groq LLM API for AI-powered responses.
- Stores Groq API key securely in `.env`.
- Implements clarifying question logic if user input is ambiguous.
- Placeholder for business logic to query e-commerce data and provide smart responses.

### 6. Frontend Implementation
- React app (PWA) created for chat UI.
- Connects to backend `/api/chat` endpoint.
- Core chat window, message display, user input, and session persistence.

### 7. Client-side State Management
- Uses React Context API to manage message list, loading status, and user input value.
- Centralizes state for scalability and maintainability.

### 8. Conversation History Panel
- Modern sidebar UI displays all past user sessions.
- Users can click a session to load its full chat history instantly.
- Fully integrated with backend session APIs.

## Tech Stack

- Backend: FastAPI (Python)
- Database: SQLite (default) or PostgreSQL (optional)
- LLM: Groq API
- Frontend: React (PWA)

## Getting Started

### 1. Dockerized Deployment (Recommended)

The easiest way to run the full stack is with Docker Compose. This will launch the PostgreSQL database, backend, and frontend services together.

#### Prerequisites
- [Docker](https://www.docker.com/get-started) and [Docker Compose](https://docs.docker.com/compose/) installed
- Groq API key (get yours from https://console.groq.com/)

#### Steps
1. Clone the repository and navigate to the project root.
2. Create a `.env` file at the project root with your API key:
   ```sh
   echo GROQ_API_KEY=your_groq_api_key > .env
   ```
3. Start all services:
   ```sh
   docker-compose up --build
   ```
   - The backend will be available at [http://localhost:8000](http://localhost:8000)
   - The frontend will be available at [http://localhost:3000](http://localhost:3000)
   - PostgreSQL database runs in a container
4. (First time only) Ingest data into the database:
   ```sh
   docker-compose exec backend python load_data.py
   ```

### 2. Manual Local Setup (Advanced)

If you prefer to run services manually:

#### Backend
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

#### Frontend
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

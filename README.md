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
- [x] Milestone 7: Client-side State Management
- [x] Milestone 8: Conversation History Panel
- [x] Milestone 9: Full-Stack Integration
- [x] Milestone 10: Dockerization

## Milestone Details

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

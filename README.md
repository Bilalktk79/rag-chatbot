#  RAG Chatbot

An AI-powered **Retrieval-Augmented Generation (RAG)** chatbot built using **FastAPI**, **React**, **FAISS**, and modern AI/NLP workflows.
This chatbot allows users to upload documents, perform semantic search, and receive contextual AI-generated responses in real time.

---

#  Features

*  User Authentication System
*  Document Upload & Processing
*  Retrieval-Augmented Generation (RAG)
*  Semantic Search with FAISS Vector Store
*  AI Chat Interface
*  Chat Memory Management
*  FastAPI Backend APIs
*  Modern React + Tailwind Frontend
*  Modular Project Architecture
*  Context-Aware Responses
*  Secure Backend Structure

---

#  Tech Stack

## Frontend

* React + Vite
* Tailwind CSS
* Axios
* React Router

## Backend

* FastAPI
* Python
* FAISS Vector Database
* SQLite / MongoDB
* JWT Authentication

## AI / NLP

* RAG Pipeline
* Embeddings
* Semantic Retrieval
* Contextual AI Responses

---

#  Project Structure

```bash
rag_chatbot/
│
├── backend/
│   ├── app/
│   ├── data/
│   ├── vector_store/
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   ├── public/
│   └── package.json
│
└── README.md
```

---

#  Installation

##  Clone Repository

```bash
git clone https://github.com/Bilalktk79/rag-chatbot.git
cd rag-chatbot
```

---

#  Backend Setup

```bash
cd backend

python -m venv venv
```

### Activate Virtual Environment

#### Windows

```bash
venv\Scripts\activate
```

#### Mac/Linux

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Backend Server

```bash
uvicorn app.main:app --reload
```

Backend will run on:

```bash
http://127.0.0.1:8000
```

---

#  Frontend Setup

Open another terminal:

```bash
cd frontend
npm install
npm run dev
```

Frontend will run on:

```bash
http://localhost:5173
```

---

#  How RAG Works

1. User uploads documents
2. Documents are chunked and embedded
3. Embeddings stored in FAISS vector database
4. User asks question
5. Relevant chunks retrieved semantically
6. AI generates contextual response

---

#  Environment Variables

Create `.env` file inside backend:

```env
OPENAI_API_KEY=your_api_key
MONGO_URI=your_mongodb_uri
SECRET_KEY=your_secret_key
```

---

#  Future Improvements

* Voice Chat Integration
* PDF Summarization
* Multi-Document Search
* Streaming Responses
* Docker Deployment
* Admin Dashboard
* Chat History Persistence

---

#  Author

Bilal

GitHub:
https://github.com/Bilalktk79

---

#  Support

If you like this project, give it a ⭐ on GitHub.

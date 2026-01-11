# 🧘 Yoga RAG App  
**Ask Me Anything About Yoga using Retrieval-Augmented Generation**

---

## 📌 Overview

The **Yoga RAG App** is an AI-powered question-answering system that allows users to ask natural, real-world questions about yoga (including imperfect grammar) and receive accurate, source-grounded answers.

The system uses **Retrieval-Augmented Generation (RAG)** to reduce hallucinations by retrieving relevant information from a curated yoga knowledge base before generating responses.

---

## ✨ Key Features

- 🧠 RAG-based architecture (retrieval + generation)
- 🔍 Semantic search using vector embeddings
- 🧘 Covers:
  - Yoga asanas
  - Uses & benefits
  - Side effects & contraindications
  - Who can / should not practice
  - Stress, sleep, digestion, posture, anxiety
- ❓ Handles user-style and grammatically incorrect questions
- 📚 Source citations shown for every answer
- ⚡ Fast local execution

---

## 🏗️ Architecture

User Question  
↓  
Text Embedding (SentenceTransformer)  
↓  
Vector Search (MongoDB)  
↓  
Relevant Knowledge Chunks  
↓  
LLM Answer Generation  
↓  
Answer + Sources  

---

## 🧰 Tech Stack

### Backend
- Python
- MongoDB (Vector Store)
- SentenceTransformers
- NumPy

### Frontend
- React
- Tailwind CSS

### AI / ML
- Embedding Model: `all-MiniLM-L6-v2`
- Vector Dimension: 384
- Similarity Metric: Cosine Similarity

---

## 📂 Project Structure
yoga-rag-micro-app/
├── backend/
│ ├── rag/
│ │ ├── ingest_mongo.py
│ │ ├── retriever.py
│ │ └── answer_generator.py
│ ├── vectorstore/
│ │ ├── yoga_articles.json
│ │ ├── yoga_asanas.json
│ │ ├── yoga_asanas_complete.json
│ │ ├── yoga_asanas_detailed.json
│ │ ├── yoga_qa_pairs.json
│ │ └── yoga_qa_pairs1.json
│ └── requirements.txt
├── frontend/
│ └── src/
└── README.md


---

## 📚 Knowledge Base

The application uses structured JSON files as its knowledge source, including:

- Yoga articles  
- Detailed asana descriptions  
- User-style question–answer pairs  
- Safety guidelines and contraindications  

All content is vectorized and indexed for semantic retrieval.

---

## 🚀 Setup & Installation

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/spirit2103/yoga-rag-micro-app.git
cd yoga-rag-micro-app
```
### 2️⃣ Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate
# Windows: venv\Scripts\activate
```
### 3️⃣ Install Backend Dependencies
```bash 
pip install -r backend/requirements.txt
```
### 4️⃣ Start MongoDB
```bash 
mongod
```

### 5️⃣ Ingest Knowledge into MongoDB
```bash
cd backend
python rag/ingest_mongo.py
```

### 6️⃣ Run Backend
```bash
cd backend
uvicorn app:app --reload --port 5000
```
### 7️⃣ Run Frontend
```bash
cd frontend
npm install
npm run dev
```
##### Open in browser:
```bash
👉 http://localhost:3000
```

## 🧪 Example Questions

**what is the uses of shavasana**
**which asana good for stress**
**who should not do bhujangasana**
**which yoga helps for sleep**
**what yoga pose helps digestion**

## 🧾 Example Output

#### Question:
which asana good for stress

#### Answer:
Shavasana is ideal for reducing stress because it relaxes the nervous system and calms the mind.

#### Sources Used:

**yoga_qa_pairs.json**

**yoga_asanas_complete.json**

## 👨‍💻 Author
**Sushanth D**
AI Engineer | RAG Systems | Applied AI
# 💙 Mental Health AI Support System (Enterprise Edition)

[![CI Pipeline](https://github.com/LEVELING2108/Mental-health-ai/actions/workflows/ci.yml/badge.svg)](https://github.com/LEVELING2108/Mental-health-ai/actions)
[![FastAPI](https://img.shields.io/badge/API-FastAPI-009688?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/Frontend-React-61DAFB?style=flat&logo=react&logoColor=black)](https://reactjs.org/)
[![Python 3.12](https://img.shields.io/badge/Python-3.12-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A high-performance, end-to-end production-grade AI system designed to provide empathetic mental health support through hybrid machine learning architectures.

## 🎯 Project Overview
This project transcends basic sentiment analysis by combining specialized classification models with state-of-the-art Transformers (DistilBERT) and Generative LLMs (FLAN-T5). It offers a safe, explainable, and context-aware platform for mental health risk detection and supportive intervention.

## 🧱 Hybrid AI Architecture
1.  **Specialized Classifier:** A Logistic Regression model with TF-IDF vectorization, trained on a custom dataset for high-accuracy risk detection (Low, Medium, High).
2.  **Emotion Transformer:** Integrated **DistilBERT** (Hugging Face) to detect nuanced emotional states (Joy, Sadness, Fear, Anger, Surprise, Love).
3.  **Generative AI Layer:** Employs **FLAN-T5-Base** to generate human-like, context-aware empathetic responses based on detected risks and emotions.
4.  **Knowledge Injection:** A keyword-specific guidance system that injects expert-level context (Anxiety, Grief, Work-stress, etc.) into the AI's generation process.

## 📁 Project Structure
```text
Mental_Health_AI/
├── api/                  # FastAPI Backend Architecture
│   ├── routes/           # Decoupled Endpoint Controllers
│   ├── schemas/          # Strict Pydantic Data Models
│   └── main.py           # API Gateway & Middleware
├── core/                 # Enterprise Core (Config, Logging, Settings)
├── frontend/             # Modern React (TS) + Vite Frontend
├── model/                # ML Implementation & Classifiers
├── utils/                # Utility Modules
│   ├── generator.py      # LLM & Knowledge Base Logic
│   ├── response.py       # Safety-checked Rule Engine
│   └── explain.py        # TF-IDF Explainability Helpers
├── data/                 # Curated Training Datasets
├── tests/                # Comprehensive Test Suite (Pytest)
├── Dockerfile            # Multi-stage Docker Build
└── docker-compose.yml    # Full-stack Orchestration
```

## 🛠 Technologies
- **Backend:** Python, FastAPI, Pydantic, Uvicorn, Scikit-learn, Joblib.
- **Deep Learning:** PyTorch, Hugging Face Transformers (DistilBERT, FLAN-T5).
- **Frontend:** React 18+, TypeScript, Vite, Vanilla CSS.
- **DevOps:** Docker, Docker Compose, GitHub Actions (CI), Ruff (Linting).

## 🚀 Getting Started

### Prerequisites
- Python 3.12+
- Node.js & npm

### Backend Setup
1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
2. **Train Classifier:**
   ```bash
   python model/train.py
   ```
3. **Run API:**
   ```bash
   uvicorn api.main:app --reload --port 8001
   ```

### Frontend Setup
1. **Navigate to Frontend:**
   ```bash
   cd frontend
   ```
2. **Install & Run:**
   ```bash
   npm install
   npm run dev
   ```

## 🔥 Key Enterprise Features
- **Explainability:** Real-time keyword extraction to show "why" the AI flagged a specific risk level.
- **Hybrid Logic:** Sentiment-based risk escalation for enhanced safety.
- **Decoupled Scaling:** Backend and Frontend communicate via a secure REST API.
- **Crisis Intervention:** Automatic detection of high-risk keywords triggers immediate display of crisis resources.
- **Production-Ready:** Includes structured logging, environment configuration, and containerization.

---
**Disclaimer:** *This AI tool is for informational and educational purposes only. It is not a substitute for professional mental health advice, diagnosis, or treatment.*

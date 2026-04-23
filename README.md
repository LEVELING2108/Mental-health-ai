# 💙 Sentimental AI: Enterprise Mental Health Support (Tier 1)

[![CI Pipeline](https://github.com/LEVELING2108/Mental-health-ai/actions/workflows/ci.yml/badge.svg)](https://github.com/LEVELING2108/Mental-health-ai/actions)
[![FastAPI](https://img.shields.io/badge/API-FastAPI-009688?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/Frontend-React-61DAFB?style=flat&logo=react&logoColor=black)](https://reactjs.org/)
[![Database](https://img.shields.io/badge/Database-SQLAlchemy-D71F00?style=flat&logo=sqlalchemy&logoColor=white)](https://www.sqlalchemy.org/)
[![AI-Brain](https://img.shields.io/badge/AI-Transformers-FFD21E?style=flat&logo=huggingface&logoColor=black)](https://huggingface.co/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Sentimental AI** is a world-class, production-grade mental health platform that leverages a hybrid of Zero-Shot Classification and Generative AI to provide empathetic, context-aware support. This system is designed with an "Enterprise-First" mindset, featuring secure authentication, multi-modal voice input, and data-driven mood analytics.

## 🌟 Tier 1 "Killer" Features

### 1. 🎙️ Multi-Modal Intelligence
*   **Speech-to-Text Integration:** Users can speak their feelings directly through a high-precision voice recognition system.
*   **Zero-Shot Classifier:** Powered by `facebook/bart-large-mnli`, the system understands complex clinical patterns (Depression, Anxiety, Suicidal Ideation) without needing massive niche datasets.
*   **Emotion Transformer:** Detects 6 core emotional states (Joy, Sadness, Fear, Anger, Surprise, Love) using `distilbert-base-uncased-emotion`.

### 2. 📊 Actionable Mood Analytics
*   **"My Journey" Dashboard:** Interactive data visualizations built with **Recharts**.
*   **Risk Trends:** Area charts visualizing mental health risk levels over time.
*   **Emotional Distribution:** Bar charts showing the frequency of different emotional states.

### 3. 🛡️ Enterprise-Grade Security
*   **JWT Authentication:** Secure login and registration with JSON Web Tokens.
*   **Direct Bcrypt Hashing:** Professional-standard password encryption.
*   **Database Persistence:** Full emotional history tracking using **SQLAlchemy** and **SQLite/PostgreSQL**.

### 4. ✨ Generative Empathy
*   **Context-Aware Support:** Uses **FLAN-T5-Base** to generate unique, supportive responses.
*   **Knowledge Injection:** Automatically injects expert-level guidance for 15+ critical categories (Exam stress, Grief, Burnout, etc.).

---

## 🧱 Technical Architecture

1.  **Backend (FastAPI):** Scalable REST API with decoupled routers, schemas, and lazy-loading for AI models.
2.  **Frontend (React + Vite):** A modern, responsive sidebar-based shell with global state management via the Context API.
3.  **MLOps:** Full CI/CD pipeline via GitHub Actions, including linting (Ruff) and automated testing (Pytest).
4.  **DevOps:** Multi-stage Docker builds for secure, lightweight deployment.

---

## 📁 Project Structure
```text
Mental_Health_AI/
├── api/                  # FastAPI Backend
│   ├── routes/           # Auth, Predict, and Mood history controllers
│   ├── schemas/          # Pydantic V2 Data Models
│   └── deps.py           # JWT & DB Dependencies
├── core/                 # App Core (Security, Config, Logging)
├── db/                   # Database Models & Connections
├── alembic/              # Database Migrations
├── frontend/             # React (TS) + Vite + Recharts
├── model/                # AI Implementation (Zero-Shot, Transformers)
├── utils/                # Hybrid AI logic & Knowledge Base
├── tests/                # Comprehensive Test Suite
└── Dockerfile            # Containerization
```

## 🚀 Installation & Setup

### Prerequisites
- Python 3.12+
- Node.js & npm

### 1. Backend Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Run migrations
alembic upgrade head

# Start server
python -m uvicorn api.main:app --reload --host 127.0.0.1 --port 8001
```

### 2. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

---
**Disclaimer:** *This AI tool is for informational and educational purposes only. It is not a substitute for professional mental health advice, diagnosis, or treatment.*

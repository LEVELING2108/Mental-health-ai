# 💙 Sentimental AI: Tier 1 Enterprise Mental Health Support

[![CI Pipeline](https://github.com/LEVELING2108/Mental-health-ai/actions/workflows/ci.yml/badge.svg)](https://github.com/LEVELING2108/Mental-health-ai/actions)
[![FastAPI](https://img.shields.io/badge/API-FastAPI-009688?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/Frontend-React-61DAFB?style=flat&logo=react&logoColor=black)](https://reactjs.org/)
[![AI-Brain](https://img.shields.io/badge/AI-Transformers-FFD21E?style=flat&logo=huggingface&logoColor=black)](https://huggingface.co/)
[![Database](https://img.shields.io/badge/Database-SQLAlchemy-D71F00?style=flat&logo=sqlalchemy&logoColor=white)](https://www.sqlalchemy.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Sentimental AI** is a production-grade, clinical-aware mental health platform. It leverages a sophisticated Hybrid AI architecture (Zero-Shot + Generative Transformers) to provide empathetic, actionable support. Architected for scale and privacy, it features secure authentication, real-time analytics, and multi-modal input.

---

## 🌟 Tier 1 "Elite" Features

### 1. 🧠 Hybrid Intelligence "Brain"
*   **Zero-Shot Classifier:** Powered by `BART-Large-MNLI`, providing high-precision detection of clinical states like Depression, Anxiety, and Suicidal Ideation without niche training data.
*   **Actionable Generative AI:** Uses `FLAN-T5-Base` with a custom **Smart Recommendation Engine**. It doesn't just "talk"—it provides concrete next steps (e.g., 5-4-3-2-1 grounding, sleep hygiene) woven into empathetic responses.
*   **Emotion Transformer:** Nuanced detection of 6 core emotional states using `DistilBERT`.

### 2. 🎙️ Multi-Modal & Premium UI
*   **Voice-to-Text:** Native browser Speech Recognition for users to speak their feelings.
*   **Interactive Grounding Tool:** A high-end "Box Breathing" visual guide for immediate distress tolerance.
*   **Premium Dark Mode:** A sophisticated midnight-themed interface with smooth CSS transitions.

### 3. 📊 Enterprise Data Analytics
*   **"My Journey" Dashboard:** Professional-grade visualizations using **Recharts**.
*   **Persistence:** Secure storage of emotional history using **SQLAlchemy** (PostgreSQL/SQLite ready).
*   **Security:** JWT-based sessions with direct **Bcrypt** password encryption.

---

## 🧱 Architectural Overview

1.  **Backend (FastAPI):** High-performance asynchronous API with decoupled route management and lazy-loaded AI models.
2.  **Frontend (React + Vite + TS):** Modern, component-based architecture with global state management via Context API.
3.  **DevOps & MLOps:** 
    *   Full CI/CD via GitHub Actions.
    *   Strict quality control using **Ruff** (linting) and **Pytest**.
    *   Containerization via **Docker & Docker Compose**.

---

## 🚀 Setup & Installation

### Prerequisites
- Python 3.12+
- Node.js & npm

### 1. Backend Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Run migrations
alembic upgrade head

# Start API (Explicit binding for reliable local connection)
python -m uvicorn api.main:app --reload --host 127.0.0.1 --port 8001
```

### 2. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

---

## 📁 Project Structure
```text
Sentimental_AI/
├── api/            # Enterprise FastAPI structure
├── core/           # Security, Logging, and Config
├── db/             # SQLAlchemy Models & Migrations
├── frontend/       # React (TS) + Recharts + Lucide
├── model/          # Hybrid Transformer implementations
├── utils/          # Smart Recommendation Engine & Knowledge Base
└── tests/          # Robust Pytest Suite
```

---
**Disclaimer:** *This AI tool is for informational and educational purposes only. It is not a substitute for professional mental health advice, diagnosis, or treatment.*

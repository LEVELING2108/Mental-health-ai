# 💙 Mental Health AI Support System

Building a clean, demo-ready, explainable AI system for mental health risk detection and supportive response generation.

## 🎯 Goal
A tool to analyze user-inputted text for mental health risks (Low, Medium, High) and provide immediate, supportive feedback alongside crisis resources where necessary.

## 🧱 Architecture
- **Preprocessing:** Text cleaning (lowercase, punctuation removal).
- **Vectorization:** TF-IDF Vectorizer.
- **Classification:** Logistic Regression model.
- **Explainability:** Key phrase/word detection from user input.
- **Safe Response:** Rule-based generation for empathy and safety.
- **UI:** Streamlit for a smooth user interface.
- **API:** FastAPI for easy integration.

## 📁 Project Structure
```text
mental-health-ai/
│
├── app.py                # Streamlit UI
├── api.py                # FastAPI
│
├── model/
│   ├── train.py          # Script to train and save the model
│   ├── predict.py        # Prediction logic
│   ├── model.pkl         # Trained model
│   └── vectorizer.pkl    # TF-IDF vectorizer
│
├── utils/
│   ├── preprocess.py     # Text cleaning utilities
│   ├── response.py       # Supportive response generation
│   └── explain.py        # Explainability helpers
│
├── data/
│   └── dataset.csv       # Training dataset
│
├── requirements.txt      # Project dependencies
└── README.md             # This file
```

## 🚀 How to Run
1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
2. **Train the Model (Optional):**
   ```bash
   python model/train.py
   ```
3. **Run the Streamlit App:**
   ```bash
   streamlit run app.py
   ```
4. **Run the FastAPI (Optional):**
   ```bash
   python api.py
   ```

## 🔥 What makes this project “killer”
- **Explainability:** Shows which words triggered the risk level.
- **Ethics:** Clearly marked as a non-medical tool with immediate crisis resources.
- **UI & API:** Both a user-facing dashboard and a developer-ready endpoint.

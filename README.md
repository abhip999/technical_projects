# This repo contains multiple but small projects related to gen-AI
## LLM based text sumarization using Groq API - Project structure
```bash
Text_summarization/
│
├── app/
│   ├── __init__.py
│   ├── main.py              # Streamlit UI
│   ├── summarizer.py       # Core summarization logic
│   ├── utils.py            # Helper functions (chunking, cleaning)
│
├── config/
│   ├── config.py           # API keys & settings
│
├── data/                   # (Optional) sample input files
│
├── requirements.txt
├── README.md
├── .env                    # API key (not pushed to GitHub)
├── .gitignore
```

## 📄 LLM Text Summarizer (Groq API)

### 🚀 Overview
This project is an LLM-powered text summarization tool that reduces document length by ~70% while preserving key information.

Built using Groq API and LLaMA 3 model, the system efficiently summarizes long-form text using chunking and multi-stage summarization.

---

### 🧠 Features
- Summarizes long documents into concise insights
- Handles large text via chunking
- Multi-step summarization for better coherence
- Simple and interactive Streamlit UI

---

### ⚙️ Tech Stack
- Python
- Streamlit
- Groq API (LLaMA 3)
- NLTK (optional preprocessing)

---

### 🏗️ Architecture
1. Input text
2. Chunking (split into smaller parts)
3. Summarization using LLM
4. Combine summaries
5. Final refinement

---

### 📦 Installation

```bash
git clone https://github.com/abhip999/technical_projects.git
cd llm-text-summarizer

pip install -r requirements.txt
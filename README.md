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
- LangChain
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
pip install -r requirements.txt

# utilize below to go to respective folders and run the main files
cd text_summarization
cd review_summarization
cd RAG_based_QA
cd PDF_based_RAG
cd multi_agent_AI_system
cd AI_agents
cd agentic_AI


# 🤖 Multi-Agent AI Research System (AutoGPT-style)

A production-ready multi-agent AI system that performs **planning, research, synthesis, and review** using LLMs and external tools like Wikipedia, Arxiv, and DuckDuckGo.

---

## 🚀 Features

- 🧠 Planner Agent (breaks query into steps)
- 🔍 Research Agent (tool-calling: Wikipedia, Arxiv, DuckDuckGo)
- ✍️ Writer Agent (generates structured answer)
- ✅ Reviewer Agent (improves quality)
- 🔄 Controlled execution loop (AutoGPT-style but stable)
- 🖥️ Streamlit UI

---

```mermaid
graph TD
    A[User Query] --> B[Planner Agent]
    B --> C[Execution Loop]

    C --> D[Research Agent]
    D -->|Wikipedia| W[Wiki API]
    D -->|Arxiv| X[Arxiv API]
    D -->|DuckDuckGo| G[Search API]

    C --> E[Writer Agent]
    E --> F[Draft Answer]

    F --> H[Reviewer Agent]
    H --> I[Final Answer]

    I --> J[Streamlit UI]


flowchart LR
    U[User] --> P[Planner Agent]
    P --> L[Plan Steps]

    L --> R[Research Agent]
    R --> W[Wikipedia]
    R --> A[Arxiv]
    R --> D[DuckDuckGo]

    R --> WR[Writer Agent]
    WR --> DR[Draft]

    DR --> RV[Reviewer Agent]
    RV --> FA[Final Answer]

    FA --> UI[Streamlit UI]
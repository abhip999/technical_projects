import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from crewai import LLM

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL_NAME =  "llama-3.3-70b-versatile"

HF_TOKEN = os.getenv("HF_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
LLM_MODEL = "llama3"
TOP_K = 4

#LLM = ChatGroq(model=MODEL_NAME, api_key=GROQ_API_KEY)

# CrewAI LLM instance using Groq (supports tool calling)
llm_llama = LLM(
    model="groq/llama-3.3-70b-versatile",
    api_key=GROQ_API_KEY
)

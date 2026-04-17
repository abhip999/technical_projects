import streamlit as st
import pandas as pd
import json
import PyPDF2
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from config.config import GROQ_API_KEY, MODEL_NAME

# Initialize LLM
llm = ChatGroq(
    groq_api_key=GROQ_API_KEY,
    model_name=MODEL_NAME
)

# -----------------------------
# 📂 FILE PARSING FUNCTIONS
# -----------------------------

def parse_txt(file):
    return file.read().decode("utf-8")

def parse_json(file):
    data = json.load(file)
    # assume reviews stored under 'reviews'
    if isinstance(data, dict):
        data = data.get("reviews", data)
    return " ".join([str(item) for item in data])

def parse_csv(file):
    df = pd.read_csv(file)
    # assume review column exists
    col = st.selectbox("Select review column", df.columns)
    return " ".join(df[col].astype(str).tolist())

def parse_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# -----------------------------
# 🧠 SUMMARIZATION + SENTIMENT
# -----------------------------

def analyze_reviews(text):
    prompt = PromptTemplate(
        input_variables=["text"],
        template="""
        Analyze the following customer reviews and provide:

        1. Summary of key points
        2. Positive insights
        3. Negative insights

        Format:
        Summary:
        Positives:
        Negatives:

        Reviews:
        {text}
        """
    )

    chain = prompt | llm
    response = chain.invoke({"text": text})

    return response.content


# -----------------------------
# 🎨 HIGHLIGHT FUNCTION
# -----------------------------

def highlight_output(text):
    lines = text.split("\n")
    styled_text = ""

    for line in lines:
        if "positive" in line.lower():
            styled_text += f"<p style='color:green'><b>{line}</b></p>"
        elif "negative" in line.lower():
            styled_text += f"<p style='color:red'><b>{line}</b></p>"
        else:
            styled_text += f"<p>{line}</p>"

    return styled_text


# -----------------------------
# 🖥️ STREAMLIT UI
# -----------------------------

st.set_page_config(page_title="Customer Review Analyzer")

st.title("📊 Customer Review Analyzer (LLM Powered)")

uploaded_file = st.file_uploader(
    "Upload file (TXT, JSON, CSV, PDF)",
    type=["txt", "json", "csv", "pdf"]
)

if uploaded_file:
    file_type = uploaded_file.name.split(".")[-1]

    if file_type == "txt":
        text = parse_txt(uploaded_file)
    elif file_type == "json":
        text = parse_json(uploaded_file)
    elif file_type == "csv":
        text = parse_csv(uploaded_file)
    elif file_type == "pdf":
        text = parse_pdf(uploaded_file)
    else:
        st.error("Unsupported file type")
        text = ""

    if st.button("Analyze Reviews"):
        with st.spinner("Analyzing..."):
            result = analyze_reviews(text)

        st.subheader("📌 Insights")
        styled = highlight_output(result)
        st.markdown(styled, unsafe_allow_html=True)
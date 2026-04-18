import streamlit as st
import pandas as pd
import json
import PyPDF2
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from report_generator import generate_pdf
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
    Analyze the customer reviews and return at least 5 key points for both positives and negatives 
    but not equal, in the following format:

    Summary:
    <short summary>

    Positives:
    - point 1
    - point 2

    Negatives:
    - point 1
    - point 2

    Reviews:
    {text}
    """
)

    chain = prompt | llm
    response = chain.invoke({"text": text})

    return response.content


def extract_points(text, section):
    lines = text.split("\n")
    points = []
    capture = False

    for line in lines:
        if section.lower() in line.lower():
            capture = True
            continue
        if capture:
            if line.strip().startswith("-"):
                points.append(line.replace("-", "").strip())
            elif line.strip() == "":
                break

    return points

def plot_sentiment(positives, negatives):
    import matplotlib.pyplot as plt
    import os

    labels = ["Positive", "Negative"]
    values = [len(positives), len(negatives)]

    fig, ax = plt.subplots()
    ax.bar(labels, values)
    ax.set_title("Sentiment Distribution")

    # Save for PDF
    os.makedirs("temp", exist_ok=True)
    file_path = os.path.abspath("temp/sentiment.png")
    fig.savefig(file_path)

    return fig, file_path  # ✅ return BOTH


def generate_wordcloud(text):
    from wordcloud import WordCloud
    import matplotlib.pyplot as plt
    import os

    wc = WordCloud(width=800, height=400).generate(text)

    fig, ax = plt.subplots()
    ax.imshow(wc)
    ax.axis("off")

    os.makedirs("temp", exist_ok=True)
    file_path = os.path.abspath("temp/wordcloud.png")
    fig.savefig(file_path)

    return fig, file_path  # ✅ return BOTH

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
            positives = extract_points(result, "Positives")
            negatives = extract_points(result, "Negatives")

            # Show colored insights
            st.markdown("<h3 style='color:green'>Positives</h3>", unsafe_allow_html=True)
            for p in positives:
                st.write(f"🟢 {p}")

            st.markdown("<h3 style='color:red'>Negatives</h3>", unsafe_allow_html=True)
            for n in negatives:
                st.write(f"🔴 {n}")

            # Charts
            st.subheader("📊 Sentiment Distribution")
            fig1, sentiment_img = plot_sentiment(positives, negatives)

            st.subheader("☁️ Word Cloud")
            fig2, wordcloud_img = generate_wordcloud(" ".join(positives + negatives))

            # After analysis
            summary = result.split("Positives")[0]  # simple extraction
            # Generate charts
            fig1, sentiment_img = plot_sentiment(positives, negatives)
            fig2, wordcloud_img = generate_wordcloud(" ".join(positives + negatives))
            # ✅ Show in UI
            st.pyplot(fig1)
            st.pyplot(fig2)
            pdf_path = generate_pdf(summary, positives, negatives, sentiment_img, wordcloud_img)

            with open(pdf_path, "rb") as f:
                st.download_button(
                    label="📥 Download Full Report",
                    data=f,
                    file_name="review_analysis.pdf",
                    mime="application/pdf"
                )
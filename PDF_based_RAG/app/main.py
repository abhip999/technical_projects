import streamlit as st

from loaders import load_documents
from rag_pipeline import build_vectorstore, load_vectorstore, build_chain

from langchain.callbacks.base import BaseCallbackHandler


# =========================
# 🔄 Streaming Handler
# =========================
class StreamHandler(BaseCallbackHandler):
    def __init__(self, container):
        self.container = container
        self.text = ""

    def on_llm_new_token(self, token: str, **kwargs):
        self.text += token
        self.container.markdown(self.text + "▌")


# =========================
# 🎯 Streamlit Config
# =========================
st.set_page_config(page_title="RAG Chatbot", layout="wide")
st.title("💬 Multi-Document RAG Chatbot (Llama3)")

st.sidebar.title("📂 Upload Documents")


# =========================
# 🧠 Session State
# =========================
if "messages" not in st.session_state:
    st.session_state.messages = []

if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None


# =========================
# 📤 File Upload
# =========================
uploaded_files = st.sidebar.file_uploader(
    "Upload files",
    type=["pdf", "docx", "csv", "pptx"],
    accept_multiple_files=True
)


# =========================
# ⚙️ Process Files
# =========================
if st.sidebar.button("Process Documents"):
    if not uploaded_files:
        st.sidebar.warning("Please upload files first.")
    else:
        with st.spinner("Processing documents..."):

            docs = load_documents(uploaded_files)

            vectorstore = build_vectorstore(docs)
            st.session_state.vectorstore = vectorstore

            st.sidebar.success("✅ Documents processed successfully!")


# =========================
# 🔄 Load Existing Vectorstore
# =========================
if st.sidebar.button("Load Existing Index"):
    try:
        st.session_state.vectorstore = load_vectorstore()
        st.sidebar.success("✅ Loaded saved vectorstore!")
    except:
        st.sidebar.error("❌ No saved index found.")


# =========================
# 💬 Chat History Display
# =========================
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


# =========================
# 🧠 Chat Input
# =========================
if prompt := st.chat_input("Ask something about your documents..."):

    if st.session_state.vectorstore is None:
        st.warning("⚠️ Please upload and process documents first.")
        st.stop()

    # User message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Assistant response
    with st.chat_message("assistant"):

        stream_container = st.empty()
        handler = StreamHandler(stream_container)

        # Build chain (with streaming)
        chain = build_chain(st.session_state.vectorstore, handler)

        result = chain({"question": prompt})

        answer = result["answer"]
        sources = result["source_documents"]

        # Save response
        st.session_state.messages.append(
            {"role": "assistant", "content": answer}
        )

        # 📚 Citations Section
        with st.expander("📚 Sources"):
            for i, doc in enumerate(sources):
                source = doc.metadata.get("source", "Unknown")
                page = doc.metadata.get("page", "N/A")

                st.markdown(f"**Source {i+1}:** {source} | Page: {page}")
                st.markdown(doc.page_content[:300] + "...")


# =========================
# 🧹 Clear Chat
# =========================
if st.sidebar.button("Clear Chat"):
    st.session_state.messages = []
    st.rerun()
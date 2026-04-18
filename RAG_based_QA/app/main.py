import streamlit as st
import tempfile
import os

from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS

from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory

# Page config
st.set_page_config(page_title="RAG Chat App", layout="wide")
st.title("💬 RAG Chat with Multi-Docs")

# Load API key
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

# Session state init
if "vector_store" not in st.session_state:
    st.session_state.vector_store = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "memory" not in st.session_state:
    st.session_state.memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True
    )

# Upload multiple PDFs
uploaded_files = st.file_uploader(
    "Upload PDFs",
    type="pdf",
    accept_multiple_files=True
)

if uploaded_files:
    if st.button("Process Documents"):
        with st.spinner("Processing documents..."):

            all_docs = []

            for uploaded_file in uploaded_files:
                with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                    tmp_file.write(uploaded_file.read())
                    file_path = tmp_file.name

                loader = PyPDFLoader(file_path)
                documents = loader.load()
                all_docs.extend(documents)

            # Split
            splitter = CharacterTextSplitter(
                chunk_size=500,
                chunk_overlap=50
            )
            docs = splitter.split_documents(all_docs)

            # Embeddings
            embedding = HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2"
            )

            # Vector store
            vector_store = FAISS.from_documents(docs, embedding)

            st.session_state.vector_store = vector_store

        st.success("All documents processed!")

# Chat UI
if st.session_state.vector_store:

    llm = ChatOpenAI(temperature=0)

    qa_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=st.session_state.vector_store.as_retriever(),
        memory=st.session_state.memory
    )

    # Chat input
    user_query = st.chat_input("Ask something about your documents...")

    if user_query:
        result = qa_chain({"question": user_query})

        st.session_state.chat_history.append(("user", user_query))
        st.session_state.chat_history.append(("assistant", result["answer"]))

    # Display chat
    for role, message in st.session_state.chat_history:
        with st.chat_message(role):
            st.write(message)
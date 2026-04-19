from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.llms import Ollama

import os
from config.config import *


def build_vectorstore(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )
    chunks = splitter.split_documents(documents)

    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

    db = FAISS.from_documents(chunks, embeddings)
    db.save_local("vectorstore")

    return db


def load_vectorstore():
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    return FAISS.load_local("vectorstore", embeddings, allow_dangerous_deserialization=True)


def build_chain(vectorstore, handler):
    llm = Ollama(
        model=LLM_MODEL,
        # streaming=True,
        callbacks=[handler]
    )

    memory = ConversationBufferMemory(
        memory_key="chat_history",
        output_key="answer", 
        return_messages=True
    )

    return ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(search_kwargs={"k": TOP_K}),
        memory=memory,
        return_source_documents=True
    )
import os
import pandas as pd
from langchain.document_loaders import (
    PyPDFLoader,
    UnstructuredWordDocumentLoader,
    UnstructuredPowerPointLoader
)
from langchain.schema import Document

def load_documents(files):
    docs = []
    os.makedirs("temp", exist_ok=True)

    for file in files:
        path = os.path.join("temp", file.name)

        with open(path, "wb") as f:
            f.write(file.getbuffer())

        if file.name.endswith(".pdf"):
            loader = PyPDFLoader(path)
            loaded = loader.load()

        elif file.name.endswith(".docx"):
            loader = UnstructuredWordDocumentLoader(path)
            loaded = loader.load()

        elif file.name.endswith(".pptx"):
            loader = UnstructuredPowerPointLoader(path)
            loaded = loader.load()

        elif file.name.endswith(".csv"):
            df = pd.read_csv(path)
            loaded = [
                Document(
                    page_content=", ".join([f"{c}: {row[c]}" for c in df.columns]),
                    metadata={"source": file.name}
                )
                for _, row in df.iterrows()
            ]
        else:
            continue

        for d in loaded:
            d.metadata["source"] = file.name

        docs.extend(loaded)

    return docs
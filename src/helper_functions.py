from pathlib import Path
from langchain_core.documents import Document
from langchain_core.document_loaders import BaseLoader
import numpy as np
from langchain_core.embeddings import Embeddings
from langchain_ollama import OllamaEmbeddings


## loads a pdf document as a list of docs
def load_document(doc_path: str, loader_cls: type[BaseLoader] ) -> list[Document]:
    loader = loader_cls(doc_path)
    return loader.load()


def cosine_similarity(vec1, vec2):
    dot_product = np.dot(vec1, vec2)
    norm_vec1 = np.linalg.norm(vec1)
    norm_vec2 = np.linalg.norm(vec2)
    return dot_product / (norm_vec1 * norm_vec2)


class NomicEmbeddings(Embeddings):
    def __init__(self):
        self.model = OllamaEmbeddings(model="nomic-embed-text")

    def embed_documents(self, texts):
        prefixed_texts = [
            f"search_document: {text}" for text in texts
        ]
        return self.model.embed_documents(prefixed_texts)

    def embed_query(self, text):
        return self.model.embed_query(
            f"search_query: {text}"
        )


def format_doc(doc):
    return (
        f"Source: {Path(doc.metadata["source"]).name} "
        f"(Page: {doc.metadata.get('page_label', 'N/A')})\n"
        f"{doc.page_content}"
    )
    
def format_docs(docs):
    return "\n\n---\n\n".join(
        format_doc(doc) for doc in docs
    )
from langchain_community.document_loaders import PyPDFLoader
from helper_functions import load_document, NomicEmbeddings
from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from pathlib import Path
import time



## get paths of all relevant documents
PROJECT_ROOT = Path(__file__).resolve().parent.parent
docs_dir = PROJECT_ROOT / "documents"

paths = [str(p) for p in docs_dir.iterdir() if p.is_file() and p.suffix.lower() == ".pdf"]

## collect all documents together and get rid of empty docs
all_docs = []
for path in paths:
    docs = load_document(path, PyPDFLoader)
    all_docs.extend(docs)
    

filtered_docs = [
    doc for doc in all_docs
    if doc.page_content.strip()
]


## split docs into chunks
splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=150,
    add_start_index=True
)

chunked_docs = splitter.split_documents(filtered_docs)

## instantiate ollama embedding model
embeddings = NomicEmbeddings()

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
DB_DIR = DATA_DIR / "chroma_nomic_db"

vector_store = Chroma(
    collection_name="game_theory_books",
    embedding_function=embeddings,
    persist_directory=DB_DIR,
)

## add embedded chunks of documents to chroma db
start = time.time()

batch_size = 100

for i in range(0, len(chunked_docs), batch_size):
    batch = chunked_docs[i:i + batch_size]

    vector_store.add_documents(documents=batch)

    print(
        f"Indexed {min(i + batch_size, len(chunked_docs))}"
        f" / {len(chunked_docs)} chunks"
    )

elapsed = time.time() - start

print(f"Total indexing time: {elapsed / 60:.2f} minutes")
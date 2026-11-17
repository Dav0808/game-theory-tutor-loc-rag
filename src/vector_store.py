from pathlib import Path
from langchain_chroma import Chroma
from .helper_functions import NomicEmbeddings, format_docs

embeddings = NomicEmbeddings()

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
DB_DIR = DATA_DIR / "chroma_nomic_db"

vector_store = Chroma(
    collection_name="game_theory_books",
    embedding_function=embeddings,
    persist_directory=DB_DIR,
)


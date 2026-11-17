# Local Game Theory RAG Tutor

A locally running Retrieval-Augmented Generation (RAG) application that answers questions about game theory using a collection of academic books and lecture notes.

The project combines semantic search over game theory documents with a locally hosted large language model. Its goal is to provide context-grounded answers while keeping document processing, embeddings, retrieval, and text generation local.

**Project status:** Working prototype. A systematic evaluation of retrieval quality and generated answers is currently in progress.

## 1. Overview

The application allows users to ask questions about game theory through a command-line interface.

Rather than relying only on the language model's parametric knowledge, the system retrieves relevant passages from a collection of game theory documents and supplies them as context for answer generation.

The current implementation uses:

- **LLM:** Qwen3 8B, served locally through Ollama.
- **Embedding model:** Nomic Embed Text, served locally through Ollama.
- **Vector database:** ChromaDB.
- **RAG framework:** LangChain.

No paid LLM APIs are required.

## 2. Architecture

The application follows a standard RAG workflow:

1. **Document loading:** PDF books and lecture notes are loaded and converted into text.
2. **Text splitting:** Documents are divided into smaller, overlapping chunks.
3. **Embedding:** Each chunk is converted into a numerical vector using Nomic Embed Text.
4. **Vector storage:** Embeddings and their associated document metadata are stored in ChromaDB.
5. **Retrieval:** When a user submits a question, the system retrieves the five most relevant chunks using semantic similarity search.
6. **Generation:** Retrieved passages are passed as context to Qwen3, which generates an answer.

The indexing process is separate from the question-answering process. This means that documents do not need to be reprocessed every time the application is launched.

## 3. Technology Stack

| Component | Technology |
|---|---|
| Programming language | Python 3.13 |
| Environment and package management | uv |
| RAG framework | LangChain |
| Language model | Qwen3 8B |
| Embedding model | Nomic Embed Text |
| Local model runtime | Ollama |
| Vector database | ChromaDB |
| Document format | PDF |

## 4. Project Structure

```text
game_theory_tutor_loc_rag/
│
├── data/
│   └── chroma_nomic_db/       # Persisted ChromaDB database
│
├── documents/                 # Game theory books and lecture notes
│
├── src/
│   ├── __init__.py
│   ├── index_data.py          # Document loading, splitting and indexing
│   ├── vector_store.py        # Connection to the persisted vector database
│   ├── helper_functions.py    # Reusable helper functions
│   └── rag_pypeline.py        # RAG chain and answer generation
│
├── main.py                    # Command-line interface
├── pyproject.toml
├── uv.lock
└── README.md
```

## 5. Installation and Setup

### Prerequisites

- Python 3.13 or later
- [uv](https://docs.astral.sh/uv/)
- [Ollama](https://ollama.com/)

### Clone the repository

```bash
git clone https://github.com/Dav0808/game_theory_tutor_loc_rag.git
cd game_theory_tutor_loc_rag
```

### Install dependencies

```bash
uv sync
```

### Download the models

Make sure Ollama is running, then download the required models:

```bash
ollama pull nomic-embed-text
ollama pull qwen3:8b
```

## 6 Building the Vector Database

The PDF documents and the generated ChromaDB database are not included in this repository. Users must provide their own PDF documents and create the vector database locally.

### Step 1: Create the documents directory

From the project root:

```bash
mkdir documents
```

Place your PDF books and lecture notes inside this directory.

### Step 2: Download the required Ollama models

Make sure Ollama is running:

```bash
ollama pull nomic-embed-text
ollama pull qwen3:8b
```

### Step 3: Build the vector database

From the project root, execute:

```bash
cd src
uv run index_data.py
```

The indexing script will:

1. Load PDF documents from the `documents/` directory.
2. Extract and split their text into chunks.
3. Generate embeddings using Nomic Embed Text.
4. Store the resulting vectors and document metadata in ChromaDB.

The database will be persisted in:

```text
data/chroma_nomic_db/
```

Once indexing is complete, the database can be reused by the application. You do not need to repeat this process every time you run the tutor.

**Note:** Indexing time depends on the number and size of PDF documents and the available hardware.

## 7. Running the Application

After the vector database has been created, return to the project root:

```bash
cd ..
uv run main.py
```

You can now enter questions in the terminal and receive answers generated using the retrieved document passages.

To exit, type:

```text
exit
```

## 8. Current Status and Future Work

The current implementation provides an end-to-end local RAG pipeline, including document ingestion, vector indexing, semantic retrieval, and answer generation.

The next stage focuses on systematic evaluation.

Planned evaluation tasks include:

- **Retrieval evaluation:** measuring whether relevant document passages are retrieved for a given question.
- **Answer quality:** assessing the correctness and completeness of generated answers.
- **Grounding:** checking whether generated answers are supported by the retrieved context.
- **Error analysis:** identifying weaknesses in document processing, chunking, retrieval, and generation.

The objective is to develop a reproducible evaluation framework and use the results to identify potential improvements to the system.

## 9. Limitations

This is an experimental project rather than a production-ready application.

In particular:

- Retrieval and generation quality have not yet been comprehensively evaluated.
- PDF text extraction quality can vary across documents.
- The system's performance depends on the available hardware and local model configuration.
- Retrieved passages do not guarantee that generated answers are fully supported by the source material.

Evaluation results and further improvements will be documented as the project develops.

## 10. Document Sources and Attribution

The project uses academic books and lecture notes on game theory for document retrieval and answer generation.

Some materials are distributed under the Creative Commons Attribution-NonCommercial-NoDerivs 4.0 International license (CC BY-NC-ND 4.0).

These materials are shared in their original, unmodified form. Attribution is provided in accordance with the respective authors' licensing requirements.

License: https://creativecommons.org/licenses/by-nc-nd/4.0/

The copyright and licensing terms of each source document remain with its respective authors or rights holders. The project itself does not claim ownership of these materials.


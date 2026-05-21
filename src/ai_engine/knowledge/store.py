import logging
from importlib.util import find_spec

from src.ai_engine.knowledge.ingest import load_documents
from src.ai_engine.knowledge.embed import get_embedding


logger = logging.getLogger(__name__)
collection = None


def is_knowledge_store_available() -> bool:
    return find_spec("chromadb") is not None


def get_collection():
    global collection

    if collection is not None:
        return collection

    if not is_knowledge_store_available():
        raise RuntimeError(
            "chromadb is not installed. Install project requirements before using chat."
        )

    import chromadb

    client = chromadb.PersistentClient(path="./chroma_db")
    collection = client.get_or_create_collection("zodiac_knowledge")
    return collection

def store_documents():
    docs = load_documents()
    db_collection = get_collection()

    for i, doc in enumerate(docs):
        embedding = get_embedding(doc)
        db_collection.upsert(
            documents=[doc],
            embeddings=[embedding],
            ids=[str(i)]
        )

    print("Stored documents in vector DB")

def test_query():
    query_embedding = get_embedding("career")

    results = get_collection().query(
        query_embeddings=[query_embedding],  
        n_results=2
    )
    print(results)

def retrieve_context(query: str):
    try:
        db_collection = get_collection()
    except RuntimeError as exc:
        logger.warning("Knowledge retrieval skipped: %s", exc)
        return []

    if db_collection.count() == 0:
        logger.info("Knowledge retrieval skipped: collection is empty.")
        return []

    query_embedding = get_embedding(query)

    results = db_collection.query(
        query_embeddings=[query_embedding],
        n_results=3
    )

    documents = results.get("documents", [[]])
    return documents[0] if documents else []

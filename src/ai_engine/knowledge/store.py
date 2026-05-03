import chromadb
from src.ai_engine.knowledge.ingest import load_documents
from src.ai_engine.knowledge.embed import get_embedding


client = chromadb.Client(
    chromadb.config.Settings(
        persist_directory="./chroma_db"
    )
)
collection = client.get_or_create_collection("zodiac_knowledge")

def store_documents():
    docs = load_documents()

    for i, doc in enumerate(docs):
        embedding = get_embedding(doc)
        collection.add(
            documents=[doc],
            embeddings=[embedding],
            ids=[str(i)]
        )

    print("Stored documents in vector DB")

def test_query():
    query_embedding = get_embedding("career")

    results = collection.query(
        query_embeddings=[query_embedding],  
        n_results=2
    )
    print(results)

def retrieve_context(query: str):

    query_embedding = get_embedding(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=3
    )

    return results["documents"][0]

from openai import OpenAI
from src.config import get_required_env

client: OpenAI | None = None


def get_client() -> OpenAI:
    global client

    if client is not None:
        return client

    client = OpenAI(api_key=get_required_env("OPENAI_API_KEY"))
    return client

def get_embedding(text: str):
    response = get_client().embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding

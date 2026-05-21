from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str
    ai_configured: bool
    auth_configured: bool
    database_configured: bool
    knowledge_store_available: bool

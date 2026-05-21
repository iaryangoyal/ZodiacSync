from pydantic import BaseModel, Field, field_validator


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000)
    session_id: int | None = None

    @field_validator("message")
    @classmethod
    def validate_message(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Message cannot be empty.")
        return value


class ChatMessageResponse(BaseModel):
    role: str
    content: str


class ChatResponse(BaseModel):
    response: str
    session_id: int


class ChatSessionResponse(BaseModel):
    id: int
    title: str
    created_at: str
    updated_at: str

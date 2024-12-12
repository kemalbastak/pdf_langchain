from pydantic import BaseModel


class ChatMessage(BaseModel):
    message: str


class GeminiResponse(BaseModel):
    response: str

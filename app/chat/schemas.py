from pydantic import BaseModel

class ChatCreate(BaseModel):
    chat_id: str

class MessageSend(BaseModel):
    message: str
from typing import Dict, List
from fastapi import WebSocket

# In-memory хранилище для чатов
# chats: Dict[str, List[WebSocket]] = {}
class ChatManager:
    chats: Dict[str, Dict[str, WebSocket]] = {}  # Теперь это атрибут класса

    @staticmethod
    async def add_user_to_chat(chat_id: str, websocket: WebSocket, username: str):
        if chat_id not in ChatManager.chats:
            ChatManager.chats[chat_id] = {}
        ChatManager.chats[chat_id][username] = websocket

    @staticmethod
    async def remove_user_from_chat(chat_id: str, websocket: WebSocket):
        if chat_id in ChatManager.chats:
            ChatManager.chats[chat_id] = {u: ws for u, ws in ChatManager.chats[chat_id].items() if ws != websocket}
            if not ChatManager.chats[chat_id]:  # Если чат пуст, удаляем
                del ChatManager.chats[chat_id]

    @staticmethod
    async def broadcast_message(chat_id: str, message: str):
        if chat_id in ChatManager.chats:
            for client in ChatManager.chats[chat_id].values():
                await client.send_text(message)
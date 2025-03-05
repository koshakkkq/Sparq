from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, Query, HTTPException, Request, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from .manager import ChatManager
from ..auth.dependencies import get_current_user, get_current_user_chat
from ..auth.session import get_session
from starlette.websockets import WebSocketClose


router = APIRouter(prefix="/chat", tags=["chat"])
templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
async def chat_interface(request: Request, current_user: str = Depends(get_current_user_chat)):
    return templates.TemplateResponse("chat.html", {"request": request, "user": current_user})

@router.websocket("/ws/{chat_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    chat_id: str,
    username: str = Query(...),
):
    await websocket.accept()

    if chat_id not in ChatManager.chats:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    await ChatManager.add_user_to_chat(chat_id, websocket, username)

    try:
        while True:
            data = await websocket.receive_json()
            message = data.get("message")
            if message:
                await ChatManager.broadcast_message(chat_id, f"{username}: {message}")

    except WebSocketDisconnect:
        await ChatManager.remove_user_from_chat(chat_id, websocket)
        await ChatManager.broadcast_message(
            chat_id,f"System: {username} покинул чат"
        )


@router.post("/create/{chat_id}")
async def create_chat(chat_id: str, request: Request, current_user: str = Depends(get_current_user_chat)):

    if chat_id in ChatManager.chats:
        raise HTTPException(status_code=400, detail="Chat already exists")
    ChatManager.chats[chat_id] = {}
    return {"message": f"Chat {chat_id} created by {current_user}"}

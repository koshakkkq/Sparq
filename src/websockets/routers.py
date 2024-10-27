from fastapi import Request, WebSocket, WebSocketDisconnect, APIRouter
from fastapi.responses import HTMLResponse

from main import events_queue, templates, ws_procceser


router = APIRouter(prefix="/", tags=["chat"])


# Веб-страница для входа в чат
@router.get("/chat_test", response_class=HTMLResponse)
async def chat_interface(request: Request):
    return templates.TemplateResponse(request, "chat.html")


@router.websocket("/ws")
async def create_webscoket_connection(ws: WebSocket):
    username = ws.cookies.get("username")
    if not username:
        return

    await ws.accept()

    events_queue.connections.append((ws, username))
    try:
        while True:
            data = await ws.receive_json()
            msq_event = await ws_procceser.process(data, username)
            await events_queue._events_queue.put(msq_event)
    except WebSocketDisconnect:
        events_queue.connections.remove((ws, username))
        pass

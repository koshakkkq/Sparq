from fastapi import Request, WebSocket, WebSocketDisconnect, APIRouter
from fastapi.responses import HTMLResponse

from main import events_queue, templates, ws_procceser, logger


router = APIRouter(prefix="/", tags=["chat"])


# Веб-страница для входа в чат
@router.get("/chat_test", response_class=HTMLResponse)
async def chat_interface(request: Request):
    return templates.TemplateResponse(request, "chat.html")


@router.websocket("/ws")
async def create_webscoket_connection(ws: WebSocket):
    username = ws.cookies.get("username")
    if not username:
        logger.warning("WebSocket connection attempt without a username.")
        return

    logger.info(f"WebSocket connection established for user: {username}")
    await ws.accept()

    events_queue.connections.append((ws, username))
    try:
        while True:
            data = await ws.receive_json()
            logger.info(f"Received data from {username}: {data}")
            msq_event = await ws_procceser.process(data, username)
            logger.debug(f"Processed event for {username}: {msq_event}")
            await events_queue._events_queue.put(msq_event)
            logger.info(f"Event queued for processing: {msq_event}")
    except WebSocketDisconnect:
        events_queue.connections.remove((ws, username))
        logger.info(f"WebSocket disconnected for user: {username}.")
        logger.debug(f"Remaining WebSocket connections: {len(events_queue.connections)}")
        pass

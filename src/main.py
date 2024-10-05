import asyncio

from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from contextlib import asynccontextmanager

from src.events_queue.events_queue import EventsQuery
from src.ws_handlers import WsHanlder

events_query = EventsQuery()


@asynccontextmanager
async def lifespan(app: FastAPI):
    asyncio.create_task(events_query.run_proccesing())
    yield
    print('Shutting down...')


app = FastAPI(lifespan=lifespan)
ws_handler = WsHanlder()


templates = Jinja2Templates(directory="templates")


# Веб-страница для входа в чат
@app.get("/chat_test", response_class=HTMLResponse)
async def chat_interface(request: Request):
    return templates.TemplateResponse(request, "chat.html")


# Веб-страница для входа в чат
@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.websocket('/ws')
async def create_webscoket_connection(ws: WebSocket):
    username = ws.cookies.get('username')
    if not username:
        return

    await ws.accept()
    # TODO: Подумать как обрабатывать подключения до всех событий в event_queue
    events_query.connections.append((ws, username))
    try:
        while True:
            data = await ws.receive_json()
            msq_event = await ws_handler.process(data, username)
            await events_query._events_query.put(msq_event)
    except WebSocketDisconnect:
        # TODO: Обрабатывать отключение
        pass

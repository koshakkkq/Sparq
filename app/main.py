import asyncio

from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession
from app.date import models
from app.database import get_db
from fastapi.staticfiles import StaticFiles
from app.users.router import router as users_router
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from app.exceptions import TokenExpiredException, TokenNoFoundException
from fastapi.exceptions import HTTPException

from app.events_queue.events_queue import EventsQuery
from app.ws_handlers import WsHanlder
from datetime import datetime

events_query = EventsQuery()


@asynccontextmanager
async def lifespan(app: FastAPI):
    asyncio.create_task(events_query.run_proccesing())
    yield
    print("Shutting down...")


app = FastAPI(lifespan=lifespan)
app.mount('/static', StaticFiles(directory='app/static'), name='static')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешить запросы с любых источников. Можете ограничить список доменов
    allow_credentials=True,
    allow_methods=["*"],  # Разрешить все методы (GET, POST, PUT, DELETE и т.д.)
    allow_headers=["*"],  # Разрешить все заголовки
)

app.include_router(users_router)


ws_handler = WsHanlder()

templates = Jinja2Templates(directory="app/templates")


# Веб-страница для входа в чат
@app.get("/chat_test", response_class=HTMLResponse)
async def chat_interface(request: Request):
    return templates.TemplateResponse(request, "chat.html")


@app.get("/")
async def redirect_to_auth():
    return RedirectResponse(url="/auth")

# @app.get("/")
# async def root():
#     return {"message": "Hello World"}

@app.exception_handler(TokenExpiredException)
async def token_expired_exception_handler(request: Request, exc: HTTPException):
    # Возвращаем редирект на страницу /auth
    return RedirectResponse(url="/auth")


# Обработчик для TokenNoFound
@app.exception_handler(TokenNoFoundException)
async def token_no_found_exception_handler(request: Request, exc: HTTPException):
    # Возвращаем редирект на страницу /auth
    return RedirectResponse(url="/auth")


@app.websocket("/ws")
async def create_webscoket_connection(ws: WebSocket):
    username = ws.cookies.get("username")
    if not username:
        return

    await ws.accept()

    events_query.connections.append((ws, username))
    try:
        while True:
            data = await ws.receive_json()
            msq_event = await ws_handler.process(data, username)
            await events_query._events_query.put(msq_event)
    except WebSocketDisconnect:
        events_query.connections.remove((ws, username))
        pass


@app.get("/add_date/")
async def add_date(db: AsyncSession = Depends(get_db)):
    new_entry = models.TestModel(timestamp=datetime.utcnow())

    db.add(new_entry)
    await db.commit()  # Асинхронный commit
    await db.refresh(new_entry)  # Асинхронное обновление записи

    return {"id": new_entry.id, "timestamp": new_entry.timestamp}

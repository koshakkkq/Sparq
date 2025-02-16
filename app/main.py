import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, Depends
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from fastapi.responses import HTMLResponse
from app.auth.dependencies import get_current_user
from app.config.settings import settings
from app.events_queue.events_queue import EventsQueue
from app.websockets.controllers.controller_proccesser import (
    ControllerProcesser
)
from app.routes import get_app_router

events_queue = EventsQueue()
templates = Jinja2Templates(directory="templates")


@asynccontextmanager
async def lifespan(app: FastAPI):
    asyncio.create_task(events_queue.run_proccesing())
    print("Running events queue")
    yield


def get_application() -> FastAPI:
    application = FastAPI()
    application.include_router(get_app_router())

    return application


app = get_application()
ws_procceser = ControllerProcesser()
app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)


###########################

#ЭТО ДЛЯ ТЕСТА ЛОГИНА

###########################

@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/protected", response_class=HTMLResponse)
async def protected_page(request: Request, current_user: str = Depends(get_current_user)):
    return templates.TemplateResponse("protected.html", {"request": request, "user": current_user})

@app.get('/healthchecker')
def healthchecker():
    return {"data": "alive"}
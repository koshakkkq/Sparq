import asyncio
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, Depends
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from fastapi.responses import HTMLResponse
from src.auth.dependencies import get_current_user
from src.config.settings import settings
from src.events_queue.events_queue import EventsQueue
from src.websockets.controllers.controller_proccesser import (
    ControllerProcesser
)
from src.routes import get_app_router

events_queue = EventsQueue()
templates = Jinja2Templates(directory="templates")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    asyncio.create_task(events_queue.run_proccesing())
    logger.info("Running events queue")
    routes_info = "\n".join(
        f"{', '.join(route.methods)} {route.path}"
        for route in app.routes
        if hasattr(route, "methods")
    )
    logger.info(f"Available Routes:\n{routes_info}")

    yield

def get_application() -> FastAPI:
    application = FastAPI(lifespan=lifespan)
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
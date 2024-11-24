import asyncio
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.templating import Jinja2Templates


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

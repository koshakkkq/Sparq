import asyncio
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


@asynccontextmanager
async def lifespan(app: FastAPI):
    asyncio.create_task(events_queue.run_proccesing())
    print("Running events queue")
    yield


def get_application() -> FastAPI:
    application = FastAPI(lifespan=lifespan)
    application.include_router(get_app_router())

    return application


app = get_application()
ws_procceser = ControllerProcesser()

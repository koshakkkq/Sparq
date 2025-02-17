from .events_queue import EventsQueue
from dataclasses import dataclass


@dataclass
class SendMessageToAllUsersEvent:
    msg: str

    async def process(self, msg_queue: EventsQueue):
        for ws_user, _ in msg_queue.connections:
            await ws_user.send_text(self.msg)

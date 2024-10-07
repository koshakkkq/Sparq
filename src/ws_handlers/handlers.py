from src.events_queue.events import SendMessageToAllUsersEvent
from src.main import ws_handler


@ws_handler.handler("sendMessage")
async def process_msg(data, username):
    msg = data.get("text")
    if not msg:
        return None
    return SendMessageToAllUsersEvent(username + ": " + msg)

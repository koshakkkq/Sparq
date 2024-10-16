from app.events_queue.events import SendMessageToAllUsersEvent
from app.main import ws_handler


@ws_handler.handler("sendMessage")
async def process_msg(data, username):
    msg = data.get("text")
    if not msg:
        return None
    return SendMessageToAllUsersEvent(username + ": " + msg)

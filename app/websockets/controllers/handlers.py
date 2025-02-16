from app.events_queue.events import SendMessageToAllUsersEvent
from main import ws_procceser


@ws_procceser.handler("sendMessage")
async def process_msg(data, username):
    msg = data.get("text")
    if not msg:
        return None
    return SendMessageToAllUsersEvent(username + ": " + msg)

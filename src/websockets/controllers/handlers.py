from src.events_queue.events import SendMessageToAllUsersEvent
from main import ws_procceser, logger


@ws_procceser.handler("sendMessage")
async def process_msg(data, username):
    logger.info(f"Processing message from user: {username}")
    logger.debug(f"Received data: {data}")

    msg = data.get("text")
    if not msg:
        logger.warning(f"No 'text' field found in the data from user: {username}")
        return None

    logger.info(f"Message processed for user {username}: {msg}")
    return SendMessageToAllUsersEvent(username + ": " + msg)

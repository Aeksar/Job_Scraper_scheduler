import json
from aio_pika import Message

from .conf import get_conection, setup_rabbit
from config import logger

    
async def send_message(message: Message, routing_key: str):
    conn = await get_conection()
    ch, _ = await setup_rabbit(conn)
    logger.info(f"Send message with rk -> {routing_key}")
    await ch.default_exchange.publish(
        message=message,
        routing_key=routing_key
    )
import json
from aio_pika import Message
import pika
from pika.adapters.blocking_connection import BlockingChannel

from .conf import get_conection, setup_rabbit, get_sync_connection
from config import logger, rabbit_cfg

    
async def async_send_message(message: Message, routing_key: str):
    conn = await get_conection()
    ch, _ = await setup_rabbit(conn)
    logger.info(f"Send message with rk -> {routing_key}")
    await ch.default_exchange.publish(
        message=message,
        routing_key=routing_key
    )
    
def sync_send_message(message: bytes, routing_key: str):
    logger.error(f"Sending new message to {routing_key}")
    with get_sync_connection() as conn:
        with conn.channel() as ch:
            ch: BlockingChannel = ch
            ch.queue_declare(
                queue=routing_key,
                arguments={"x-message-ttl" : rabbit_cfg.MQ_TTL},
            )
            ch.basic_publish(
                exchange="",
                routing_key=routing_key,
                body=message
            )
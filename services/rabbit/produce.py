from pika.adapters.blocking_connection import BlockingChannel

from .conf import get_connection
from config import logger, rabbit_cfg

    
def send_message(message: bytes, routing_key: str):
    logger.info(f"Sending new message to {routing_key}")
    with get_connection() as conn:
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
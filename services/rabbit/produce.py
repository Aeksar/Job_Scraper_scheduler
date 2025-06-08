import json
from aio_pika import Message

from .conf import get_conection, setup_rabbit
from config import rabbit_cfg, logger


async def send_message_to_bot(body: dict):
    global rabbit_cfg
    conn = await get_conection()
    ch, _ = await setup_rabbit(conn)
    body = json.dumps(body).encode()
    message = Message(body=body)
    logger.info(f"Send to bot -> {body}")
    await ch.default_exchange.publish(
        message=message,
        routing_key=rabbit_cfg.MQ_BOT_RK
    )
    
async def send_message_to_parser(body: dict):
    global rabbit_cfg
    conn = await get_conection()
    ch, _ = await setup_rabbit(conn)
    body = json.dumps(body).encode()
    message = Message(body=body)
    logger.info(f"Send to parser -> {body}")
    await ch.default_exchange.publish(
        message=message,
        routing_key=rabbit_cfg.MQ_PARSE_RK
    )
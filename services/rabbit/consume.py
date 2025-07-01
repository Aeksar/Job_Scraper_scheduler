from pika.spec import Basic, BasicProperties
from pika.adapters.blocking_connection import BlockingChannel
import aio_pika
import json

from services.mongo import HhCollection, SubscribeCollection, mongo_client
from services.rabbit.produce import sync_send_message
from services.rabbit.conf import setup_sync_rabbit, get_sync_connection
from config import rabbit_cfg, logger


def consumer(
    ch: BlockingChannel, 
    method: Basic.Deliver,
    properties: BasicProperties,
    body: bytes
):
        payload: dict = json.loads(body)
        params: dict = payload.get("params")
        text = params.get("text")
        city = params.get("city")
        
        sub_col = SubscribeCollection(mongo_client)
        hh_col = HhCollection(mongo_client)
        chat_ids = sub_col.get_subscribers(text, city)
        data = hh_col.find_by_ids(payload.get("data"))
        body = {
            "title": "new",
            "chat_ids": chat_ids,
            "data": data
        }
        message = json.dumps(body).encode()
        ch.basic_ack()
        sync_send_message(message, rabbit_cfg.MQ_BOT_RK)
        
def start_consume():
    with get_sync_connection() as conn:
        ch, queue = setup_sync_rabbit(conn)
        ch.basic_consume(
            queue=rabbit_cfg.MQ_CONSUME_QUEUE,
            on_message_callback=consumer
        )
        logger.debug("Start consuming messages")
        ch.start_consuming()

            
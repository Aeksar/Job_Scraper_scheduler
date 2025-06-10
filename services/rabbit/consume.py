import aio_pika
import json

from services.mongo import HhCollection, SubscribeCollection, mongo_client
from services.rabbit.produce import send_message
from services.rabbit.conf import setup_rabbit
from config import rabbit_cfg, logger
from utils import get_base_message

async def consumer(message: aio_pika.IncomingMessage):
    async with message.process():
        body = message.body.decode()
        payload: dict = json.loads(body)
        params: dict = payload.get("params")
        text = params.get("text")
        city = params.get("city")
        
        sub_col = SubscribeCollection(mongo_client)
        hh_col = HhCollection(mongo_client)
        chat_ids = await sub_col.get_subscribers(text, city)
        data = await hh_col.find_by_ids(payload.get("data"))
        body = {
            "title": "new",
            "chat_ids": chat_ids,
            "data": data
        }
        message = get_base_message(body)
        await send_message(message, rabbit_cfg.MQ_BOT_RK)
        
        
async def start_consume(conn: aio_pika.abc.AbstractConnection):
    ch, queue = await setup_rabbit(conn)
    async with queue.iterator() as queue_iter:
        async for message in queue_iter:
            try:
                await consumer(message)
            except Exception as e:
                logger.error(f"Error with process message: {e}")
            
            
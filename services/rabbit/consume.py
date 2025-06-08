import aio_pika
import json

from services.mongo import HhCollection, SubscribeCollection, mongo_client
from services.rabbit.produce import send_message_to_bot
from services.rabbit.conf import setup_rabbit
from config import logger

async def consumer(message: aio_pika.IncomingMessage):
    async with message.process():
        body = message.body.decode()
        payload: dict = json.loads(body)
        print(payload)
        params: dict = payload.get("params")
        print(params)
        text = params.get("text")
        city = params.get("city")
        print(text)
        sub_col = SubscribeCollection(mongo_client)
        hh_col = HhCollection(mongo_client)
        chat_ids = await sub_col.get_subscribers(text, city)
        data = await hh_col.find_by_ids(payload.get("data"))
        message = {
            "title": "new",
            "chat_ids": chat_ids,
            "data": data
        }
        await send_message_to_bot(message)
        
async def start_consume(conn: aio_pika.abc.AbstractConnection):
    ch, queue = await setup_rabbit(conn)
    async with queue.iterator() as queue_iter:
        async for message in queue_iter:
            # try:
                await consumer(message)
            # except Exception as e:
            #     logger.error(f"Error with process message: {e}")
            
            
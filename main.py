import asyncio

from services.rabbit import get_conection, start_consume, send_message_to_parser
from services.mongo import mongo_client, SubscribeCollection
from config import logger, NOTIFICATION_DELAY

async def task():
    while True:
        await asyncio.sleep(NOTIFICATION_DELAY)
        sub_col = SubscribeCollection(mongo_client)
        params = await sub_col.get_params()
        for param in params:
            logger.debug(f"send message to parser with parameters: {param}")
            body = {
                "title": "hh",
                "data": param,
                "only_new": True,
            }
            await send_message_to_parser(body)
        

async def main():
    conn = await get_conection()
    loop = asyncio.get_event_loop()
    asyncio.create_task(task())
    await start_consume(conn)
    loop.run_forever()
    
    

if __name__ == "__main__":
    asyncio.run(main())
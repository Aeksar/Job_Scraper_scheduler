import asyncio
import aiohttp

from services.rabbit import get_conection, start_consume, send_message
from services.mongo import mongo_client, SubscribeCollection, HhCollection
from config import rabbit_cfg, logger, NOTIFICATION_DELAY, CLEAN_DELAY, HH_VACANCIES_BASE_URL, USER_AGENT
from utils import get_base_message, hh_ids_from_urls


async def notification_task():
    while True:
        await asyncio.sleep(NOTIFICATION_DELAY)
        sub_col = SubscribeCollection(mongo_client)
        params = await sub_col.get_params()
        for param in params:
            logger.debug(f"Send message to parser with parameters: {param}")
            body = {
                "title": "hh",
                "data": param,
                "only_new": True,
            }
            message = get_base_message(body)
            await send_message(message, rabbit_cfg.MQ_PARSE_RK)
        
        
async def clean_task():
    while True:
        await asyncio.sleep(CLEAN_DELAY)
        hh_col = HhCollection(mongo_client)
        urls = await hh_col.get_urls()
        ids = hh_ids_from_urls(urls)
        headers = {"user-agent": USER_AGENT}
        async with aiohttp.ClientSession(HH_VACANCIES_BASE_URL, headers=headers) as session:
            delete_urls = []
            for id in ids:
                response = await session.get(id)
                if response.status == 200:
                    data: dict = await response.json()
                    status = data.get("archived")
                    if status:
                        delete_urls.append(str(response.url))
                else:
                    delete_urls.append(str(response.url))
        await hh_col.delete_by_urls(delete_urls)
    
    
async def main():
    conn = await get_conection()
    loop = asyncio.get_event_loop()
    asyncio.create_task(notification_task())
    asyncio.create_task(clean_task())
    await start_consume(conn)
    loop.run_forever()
    

if __name__ == "__main__":
    asyncio.run(main())
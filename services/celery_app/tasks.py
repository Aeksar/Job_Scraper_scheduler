import requests
import json
from celery import shared_task
from celery.signals import worker_ready
import threading

from services.rabbit import sync_send_message, get_sync_connection, setup_sync_rabbit, consumer
from services.mongo import sync_mongo_client, mongo_client, SubscribeCollection, HhCollection
from config import rabbit_cfg, logger, NOTIFICATION_DELAY, CLEAN_DELAY, HH_VACANCIES_BASE_URL, USER_AGENT
from utils import get_base_message, hh_ids_from_urls  


@shared_task(name="notification")
def async_notification_task():
    logger.debug("start notif task")
    sub_col = SubscribeCollection(sync_mongo_client)
    params = sub_col.get_params()
    for param in params:
        logger.debug(f"Send message to parser with parameters: {param}")
        body = {
            "title": "hh",
            "data": param,
            "options": {
                "only_new": True,
            }
        }
        message = json.dumps(body).encode()
        sync_send_message(message, rabbit_cfg.MQ_PARSE_RK)
        
@shared_task(name="clean")  
async def clean_task():
    hh_col = HhCollection(sync_mongo_client)
    urls = hh_col.get_urls()
    ids = hh_ids_from_urls(urls)
    headers = {"user-agent": USER_AGENT}
    delete_urls = []
    
    for id in ids:
        response = requests.get(HH_VACANCIES_BASE_URL+id, headers=headers)
        if response.status == 200:
            data: dict = await response.json()
            status = data.get("archived")
            if status:
                delete_urls.append(str(response.url))
        else:
            delete_urls.append(str(response.url))
            
    hh_col.delete_by_urls(delete_urls)


import aio_pika
from aio_pika.abc import AbstractConnection
from aio_pika import Message
import json

from config import rabbit_cfg, logger


async def get_conection():
    url = rabbit_cfg.get_url()
    connection =  await aio_pika.connect(url)
    logger.info("Successful connect to rabbit")
    return connection


async def setup_rabbit(connection: AbstractConnection):
    channel = await connection.channel()
    await channel.set_qos(prefetch_count=1)
    consume_queue = await channel.declare_queue(rabbit_cfg.MQ_CONSUME_QUEUE, durable=True)
    return channel, consume_queue

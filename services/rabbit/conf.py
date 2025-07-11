import pika

from config import rabbit_cfg


CONNECTION_PARAMS = pika.ConnectionParameters(
    host=rabbit_cfg.HOST,
    port=rabbit_cfg.PORT,
    credentials=pika.PlainCredentials(rabbit_cfg.USER, rabbit_cfg.PASSWORD)
)

def get_connection() -> pika.BlockingConnection:
    global CONNECTION_PARAMS
    return pika.BlockingConnection(parameters=CONNECTION_PARAMS)

def setup_rabbit(conn: pika.BlockingConnection):
    ch = conn.channel()
    ch.basic_qos(prefetch_count=1)
    queue = ch.queue_declare(
        queue=rabbit_cfg.MQ_CONSUME_QUEUE,
        durable=True,
        arguments={"x-message-ttl" : rabbit_cfg.MQ_TTL},
    )
    return ch, queue

# async def get_conection():
#     url = rabbit_cfg.get_url()
#     connection =  await aio_pika.connect(url)
#     logger.info("Successful connect to rabbit")
#     return connection


# async def setup_rabbit(connection: AbstractConnection):
#     channel = await connection.channel()
#     await channel.set_qos(prefetch_count=1)
#     consume_queue = await channel.declare_queue(rabbit_cfg.MQ_CONSUME_QUEUE, durable=True)
#     return channel, consume_queue


from celery import Celery


from config.environment import rabbit_cfg
from services.celery_app.tasks import *

"amqp://user:12568395@127.0.0.1:5672"
app = Celery(
    main="celery_app",
    broker=rabbit_cfg.get_url(),
    backend="rpc://",
    broker_connection_retry_on_startup=True
)

app.conf.timezone = 'UTC'

app.conf.beat_schedule = {
    'notification': {
        'task': 'notification',
        'schedule': 30.0,
    },
    # 'clean': {
    #     'task': 'tasks.add',
    #     'schedule': 30.0,
    #     'args': ()
    # },
}


    



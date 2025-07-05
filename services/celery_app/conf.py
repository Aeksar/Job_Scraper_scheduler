from celery import Celery


from config.environment import rabbit_cfg, NOTIFICATION_DELAY, CLEAN_DELAY
from services.celery_app.tasks import *



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
        'schedule': NOTIFICATION_DELAY,
    },
    'clean': {
        'task': 'clean',
        'schedule': CLEAN_DELAY,
        'args': ()
    },
}


    



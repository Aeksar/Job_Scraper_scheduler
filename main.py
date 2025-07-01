import threading
from celery.bin import worker

from services.celery_app.conf import app
from services.rabbit.consume import start_consume

def start_celery_worker():
    argv = ['worker', '-l', 'INFO'] # Arguments for Celery worker
    app.worker_main(argv=argv)

def main():
    threading.Thread(target=start_consume, daemon=True).start()

if __name__ == "__main__":
    main()
    import asyncio
    loop = asyncio.get_event_loop()
    loop.run_forever()
from dotenv import load_dotenv
import os


load_dotenv()

NOTIFICATION_DELAY = 86_400

class rabbit_cfg:
    HOST = os.getenv("RMQ_HOST")
    PORT = os.getenv("RMG_PORT")
    PASSWORD = os.getenv("RMQ_PWD")
    USER = os.getenv("RMQ_USER")
    MQ_PARSE_RK = os.getenv("MQ_PARSE_RK")
    MQ_BOT_RK = os.getenv("MQ_BOT_RK")
    MQ_CONSUME_QUEUE = os.getenv("MQ_CONSUME_QUEUE")

    
    @classmethod
    def get_url(cls) -> str:
        return f"amqp://{cls.USER}:{cls.PASSWORD}@{cls.HOST}:{cls.PORT}"
        
        
class mongo_cfg:
    MONGO_USERNAME=os.getenv("MONGO_INITDB_ROOT_USERNAME")
    MONGO_PASSWORD=os.getenv("MONGO_INITDB_ROOT_PASSWORD")
    MONGO_DATABASE=os.getenv("MONGO_INITDB_DATABASE")
    MONGO_HOST=os.getenv("MONGO_HOST")
    MONGO_PORT=os.getenv("MONGO_PORT")
    
    @classmethod
    def url(cls) -> str:
        return f"mongodb://{cls.MONGO_USERNAME}:{cls.MONGO_PASSWORD}@{cls.MONGO_HOST}:{cls.MONGO_PORT}/"
    
    

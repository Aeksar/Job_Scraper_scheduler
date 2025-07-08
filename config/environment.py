from dotenv import load_dotenv
import os


load_dotenv()

NOTIFICATION_DELAY = 86_400
CLEAN_DELAY = 604_800

HH_VACANCIES_BASE_URL = "https://api.hh.ru/vacancies/"
USER_AGENT = "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"

class rabbit_cfg:
    HOST = os.getenv("RMQ_HOST")
    PORT = os.getenv("RMG_PORT")
    PASSWORD = os.getenv("RMQ_PWD")
    USER = os.getenv("RMQ_USER")
    MQ_PARSE_RK = os.getenv("MQ_PARSE_RK")
    MQ_BOT_RK = os.getenv("MQ_BOT_RK")
    MQ_CONSUME_QUEUE = os.getenv("MQ_CONSUME_QUEUE")
    MQ_TTL = int(os.getenv("MQ_TTL"))
    
    @classmethod
    def get_url(cls) -> str:
        return f"amqp://{cls.USER}:{cls.PASSWORD}@{cls.HOST}:{cls.PORT}"
      

        
class mongo_cfg:
    USERNAME=os.getenv("MONGO_INITDB_ROOT_USERNAME")
    PASSWORD=os.getenv("MONGO_INITDB_ROOT_PASSWORD")
    DATABASE=os.getenv("MONGO_INITDB_DATABASE")
    HOST=os.getenv("MONGO_HOST")
    PORT=os.getenv("MONGO_PORT")
    
    @classmethod
    def url(cls) -> str:
        return f"mongodb://{cls.USERNAME}:{cls.PASSWORD}@{cls.HOST}:{cls.PORT}/"
    
    

from aio_pika import Message
import json


def get_base_message(body: dict) -> Message:
    body = json.dumps(body)
    return Message(body=body)
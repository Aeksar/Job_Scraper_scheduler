import logging


root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO) 

console_handler = logging.StreamHandler()
console_formatter = logging.Formatter('[{asctime}] #{levelname} {filename} ({lineno}): {message}', style='{')
console_handler.setFormatter(console_formatter)
root_logger.addHandler(console_handler)


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
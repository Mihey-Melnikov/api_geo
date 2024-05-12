import logging
from datetime import datetime


def get_api_logger(name):
    log_format = '%(levelname)s [%(asctime)s %(name)s] %(message)s'
    logging.basicConfig(level=logging.INFO,
                        format=log_format,
                        filename='./logger/logs/api_geo.log',
                        filemode='w',
                        encoding='utf8')
    return logging.getLogger(name)

def get_script_logger(name):
    log_format = '%(levelname)8s [%(asctime)s %(name)s] %(message)s'
    logging.basicConfig(level=logging.INFO,
                        format=log_format,
                        filename=f'./logger/logs/{name}_{str(datetime.now().strftime("%Y-%M-%d_%H-%M-%S"))}.log',
                        filemode='w',
                        encoding='utf8')
    return logging.getLogger(name)

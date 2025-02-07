import logging
logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        level=logging.INFO
    )
default_logger = logging.getLogger('default-logger')
default_logger.setLevel(logging.INFO)
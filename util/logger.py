import logging

logger = None

class Logger:
    def __init__(self, name: str = __name__) -> None:
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s [%(name)s] %(levelname)s: %(message)s"
        )
        self.logger = logging.getLogger(name)

    def info(self, message: str) -> None:
        self.logger.info(message)

    def debug(self, message: str) -> None:
        self.logger.debug(message)

    def warning(self, message: str) -> None:
        self.logger.warning(message)

    def error(self, message: str, exc_info=False) -> None:
        self.logger.error(message, exc_info=exc_info)

    def critical(self, message: str, exc_info=False) -> None:
        self.logger.critical(message, exc_info=exc_info)

def get_logger():
    global logger
    if (logger is None):
        logger = Logger('my-app')
    
    return logger
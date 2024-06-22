import logging
import colorlog

logger = None

class Logger:
    def __init__(self, name: str = None) -> None:
        name = name or __name__
        
        self.logger = logging.getLogger(name)
        self.logger.propagate = False
        self.logger.handlers.clear()

        handler = logging.StreamHandler()
        formatter = colorlog.ColoredFormatter(
            "%(log_color)s%(asctime)s [%(name)s] %(levelname)s: %(message)s",
            datefmt='%b %d %H:%M:%S',
            log_colors={
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'bold_red',
            }
        )
        handler.setFormatter(formatter)

        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(handler)

    def get_logger(self):
        return self.logger

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
    if logger is None:
        logger = Logger('shorts').get_logger()
    return logger

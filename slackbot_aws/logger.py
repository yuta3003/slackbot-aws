"""
log用モジュール
"""
from logging import Formatter, StreamHandler, getLogger, INFO


class Logger:
    """
    log定義Class
    """
    def __init__(self, name=__name__):
        self.logger = getLogger(name)
        self.logger.setLevel(INFO)
        formatter = Formatter(
            "[%(asctime)s] [%(process)d] [%(name)s] [%(levelname)s] %(message)s"
        )

        # stdout
        handler = StreamHandler()
        handler.setLevel(INFO)
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def debug(self, msg):
        """ message """
        self.logger.debug(msg)

    def info(self, msg):
        """ message """
        self.logger.info(msg)

    def warn(self, msg):
        """ message """
        self.logger.warning(msg)

    def error(self, msg):
        """ message """
        self.logger.error(msg)

    def critical(self, msg):
        """ message """
        self.logger.critical(msg)

from logging import Formatter, handlers, StreamHandler, getLogger, INFO


class Logger:
    def __init__(self, name=__name__):
        self.logger = getLogger(name)
        self.logger.setLevel(INFO)
        formatter = Formatter("[%(asctime)s] [%(process)d] [%(name)s] [%(levelname)s] %(message)s")

        # stdout
        handler = StreamHandler()
        handler.setLevel(INFO)
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def debug(self, msg):
        self.logger.debug(msg)

    def info(self, msg):
        self.logger.info(msg)

    def warn(self, msg):
        self.logger.warning(msg)

    def error(self, msg):
        self.logger.error(msg)

    def critical(self, msg):
        self.logger.critical(msg)

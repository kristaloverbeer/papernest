import logging
import os


class LoggingMixin:
    @property
    def logger(self):
        try:
            return self._logger
        except AttributeError:
            name = '.'.join([self.__class__.__module__, self.__class__.__name__])
            self._logger = logging.root.getChild(name)
            self._setup_logger()

            return self._logger

    def _setup_logger(self):
        log_format = '%(asctime)s %(levelname)-8s [%(name)s][%(funcName)s] %(message)s'

        handler = logging.StreamHandler()
        handler.formatter = logging.Formatter(log_format)

        self._logger.addHandler(handler)
        self._logger.setLevel(os.environ['LOGGING_LEVEL'])

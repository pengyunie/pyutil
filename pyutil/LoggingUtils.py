import logging
import sys
from typing import *


class LoggingUtils:

    logging_format = "[{relativeCreated:6.0f}{levelname[0]}]{name}: {message}"
    logging_format_detail = "[{asctime}|{relativeCreated:.3f}|{levelname:7}]{name}: {message} [@{filename}:{lineno}|{funcName}|pid {process}|tid {thread}]"

    # Copied from logging
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL

    @classmethod
    def get_handler_console(cls, stream=sys.stderr, level=logging.WARNING) -> logging.Handler:
        handler = logging.StreamHandler(stream=stream)
        handler.setLevel(level=level)
        handler.setFormatter(logging.Formatter(cls.logging_format, style="{"))
        return handler

    @classmethod
    def get_handler_file(cls, filename, level=logging.DEBUG) -> logging.Handler:
        handler = logging.FileHandler(filename)
        handler.setLevel(level=level)
        handler.setFormatter(logging.Formatter(cls.logging_format_detail, style="{"))
        return handler

    default_level = logging.WARNING
    default_handlers = list()

    @classmethod
    def setup(cls, level=logging.WARNING, filename: str = None):
        logging.basicConfig(level=level, format=cls.logging_format, style="{")

        cls.default_level = level
        cls.default_handlers.clear()
        cls.default_handlers.append(cls.get_handler_console(level=level))
        if filename is not None:
            cls.default_level = logging.DEBUG
            cls.default_handlers.append(cls.get_handler_file(filename=filename))
        return

    @classmethod
    def get_logger(cls, name: str,
                   level: int = None,
                   handlers: Iterable[logging.Handler] = None) -> logging.Logger:
        if level is None:
            level = cls.default_level
        # end if
        if handlers is None:
            handlers = cls.default_handlers
        # end if

        logger = logging.getLogger(name)
        logger.setLevel(level)
        logger.handlers = []
        logger.propagate = False
        for handler in handlers:
            logger.addHandler(handler)
        # end for
        return logger
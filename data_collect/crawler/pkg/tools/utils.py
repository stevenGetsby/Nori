# -*- coding: utf-8 -*-
from __future__ import annotations


import argparse
import os
import sys
from random import Random

from loguru import logger as _loguru_logger

from .crawler_util import *
from .time_util import *


# Lazy initialization flag to avoid circular import with config
_logger_initialized = False


def get_logger():
    """Get or initialize logger (lazy loading to avoid circular import)"""
    global _logger_initialized
    if _logger_initialized:
        return _loguru_logger

    # Import config here to avoid circular dependency
    import data_collect.crawler.config as config

    # Remove default handler
    _loguru_logger.remove()

    # Custom filter to add location field (file:function:line)
    def add_location(record):
        location = f"{record['file'].name}:{record['function']}:{record['line']}"
        record["extra"]["location"] = location
        return True

    # Add console handler with beautiful format (with aligned columns)
    _loguru_logger.add(
        sys.stderr,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <6}</level> | <cyan>{extra[location]: <28}</cyan> - <level>{message}</level>",
        level="INFO",
        colorize=True,
        filter=add_location
    )

    # Add file handler if enabled
    if config.ENABLE_LOG_FILE:
        # create logs dir
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        log_dir = os.path.join(project_root, 'logs', config.PLATFORM)
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        log_file = os.path.join(log_dir, f"{get_current_date()}.log")

        # Custom filter for file logging
        def add_location_file(record):
            location = f"{record['file'].name}:{record['function']}:{record['line']}"
            record["extra"]["location"] = location
            return True

        _loguru_logger.add(
            log_file,
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {extra[location]: <60} - {message}",
            level="INFO",
            encoding="utf-8",
            rotation="00:00",  # Rotate at midnight
            retention="30 days",  # Keep logs for 30 days
            filter=add_location_file
        )

    _logger_initialized = True
    return _loguru_logger


# Property-like access for backward compatibility
class LoggerProxy:
    """Proxy object that initializes logger on first access"""
    def __getattr__(self, name):
        return getattr(get_logger(), name)


logger = LoggerProxy()


def init_logging_config():
    """
    init logging config (for backward compatibility)
    Returns: logger instance
    """
    return get_logger()

def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


def get_random_str(random_len: int = 12) -> str:
    """
    获取随机字符串
    :param random_len:
    :return:
    """
    random_str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    _random = Random()
    for _ in range(random_len):
        random_str += chars[_random.randint(0, length)]
    return random_str


def random_delay_time(min_time: int = 1, max_time: int = 3) -> int:
    """
    获取随机延迟时间
    :param min_time:
    :param max_time:
    :return:
    """
    return random.randint(min_time, max_time)

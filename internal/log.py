from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys
import os
import logging
import datetime
import multiprocessing

def create_logger(name = '_default_'):
    """
    creates and returns configured logger
    """
    logger = logging.getLogger(name)
    _config_logger(logger)
    return logger

def _config_logger(logger):
    """
    config logger
    """
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('[PID %(process)d] %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

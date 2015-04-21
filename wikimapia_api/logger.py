# coding: utf-8

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
from future.utils import with_metaclass
from past.builtins import basestring
from builtins import dict
from io import open
import time

from .config import Config, LOG_LEVELS
from .errors import FunctionNameError, RequestError, UnimplementedError

class Logger(object):
    def __init__(self, config):
        if not isinstance(config, Config):
            raise TypeError('Wrong config argument')
        self._config = config

    def log(self, message, level=None, src=None):
        if not level in LOG_LEVELS:
            return
        log_level = LOG_LEVELS.index(level)
        if log_level <= 0 or log_level > LOG_LEVELS.index(self._config.log_level):
            return
        if isinstance(src, basestring):
            message = src + ': ' + message
        message = message.replace('\n', '').replace('\r', '')
        t = time.strftime('%Y-%m-%d %H:%M:%S')
        with open(self._config.log, 'at') as f:
            f.write('{0} [{1:<5s}] {2}\n'.format(t, level, message))

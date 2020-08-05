# -*- coding: utf-8 -*-
import os
import logging
import inspect
from common.baseutil import root_path, cur_date, cur_datetime

dir_folder = os.path.join(root_path, "logs", cur_date)

if not os.path.exists(dir_folder):
    os.mkdir(dir_folder)

handlers = {
    logging.DEBUG: os.path.join(dir_folder, '%s_debug.log' % cur_date),
    logging.INFO: os.path.join(dir_folder, '%s_info.log' % cur_date),
    logging.WARNING: os.path.join(dir_folder, '%s_warning.log' % cur_date),
    logging.ERROR: os.path.join(dir_folder, '%s_error.log' % cur_date),
    logging.CRITICAL: os.path.join(dir_folder, '%s_critical.log' % cur_date),
}


class Logger(object):

    def __init__(self):
        self._loggers = {}

        for level in handlers.keys():
            logger = logging.getLogger(str(level))
            logger.addHandler(logging.FileHandler(filename=handlers[level], encoding='utf-8'))
            logger.addHandler(logging.StreamHandler())
            logger.setLevel(level)
            self._loggers.update({level: logger})

    @staticmethod
    def get_log_message(level, message):
        frame, filename, line_no, function_name, code, unknown_field = inspect.stack()[2]
        return "[%s] [%s] [%s:%s - %s]: %s" % (cur_datetime, level, filename, line_no, function_name, message)

    def info(self, message):
        message = self.get_log_message("info", message)
        self._loggers[logging.INFO].info(message)

    def error(self, message):
        message = self.get_log_message("error", message)
        self._loggers[logging.ERROR].error(message)

    def warning(self, message):
        message = self.get_log_message("warning", message)
        self._loggers[logging.WARNING].warning(message)

    def debug(self, message):
        message = self.get_log_message("debug", message)
        self._loggers[logging.DEBUG].debug(message)

    def critical(self, message):
        message = self.get_log_message("critical", message)
        self._loggers[logging.CRITICAL].critical(message)


logger = Logger()

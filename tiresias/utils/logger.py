# tiresias.utils.logger
# Logging mixin classes for convenience and central configuration
#
# Author:   Allen Leis <allen.leis@gmail.com>
# Created:  Sun Apr 14 23:39:55 2019 -0400
#
# Copyright (C) 2019 Allen Leis
# For license information, see LICENSE
#
# ID: logger.py [] allen.leis@gmail.com $

"""
Logging mixin classes for convenience and central configuration
"""

##########################################################################
# Imports
##########################################################################

import os
import sys
import logging
import logging.config

logging_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {
            "format": "%(asctime)s  [%(levelname)8s]  %(message)s",
        }
    },

    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "simple",
            "stream": "ext://sys.stdout"
        },

        "info_file_handler": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "INFO",
            "formatter": "simple",
            "filename": "tiresias.info.log",
            "maxBytes": 10485760,
            "backupCount": 20,
            "encoding": "utf8"
        },

        "error_file_handler": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "ERROR",
            "formatter": "simple",
            "filename": "tiresias.errors.log",
            "maxBytes": 10485760,
            "backupCount": 20,
            "encoding": "utf8"
        }
    },

    "loggers": {
        "tiresias": {
            "level": "DEBUG",
            "handlers": ["console", "info_file_handler", "error_file_handler"],
            "propagate": False
        }
    },
}

##########################################################################
# Classes
##########################################################################

class LoggableMixin(object):
    """
    Placeholder logging mixin for eventual configuration or wrapping of global
    logging features.
    """
    def __init__(self, *args, **kwargs):
        logging.config.dictConfig(logging_config)
        self.logger = logging.getLogger('tiresias')
        super(LoggableMixin, self).__init__(*args, **kwargs)


##########################################################################
# Execution
##########################################################################

if __name__ == '__main__':
    obj = LoggableMixin()
    obj.logger.debug("Test for debug...")
    obj.logger.info("Test for info...")
    obj.logger.warning("Test for warning...")
    obj.logger.error("Test for error...")
    obj.logger.critical("Test for critical...")
    try:
        1/0
    except Exception as e:
        obj.logger.exception(e)
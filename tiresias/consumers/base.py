# tiresias.consumers.base
# Base classes for data consumers
#
# Author:   Allen Leis <allen.leis@gmail.com>
# Created:  Tue Apr 16 19:39:10 2019 -0400
#
# Copyright (C) 2017 Allen Leis
# For license information, see LICENSE
#
# ID: base.py [] allen.leis@gmail.com $

"""
Base classes for data consumers
"""

##########################################################################
# Imports
##########################################################################

from tiresias.utils.logger import LoggableMixin

##########################################################################
# Classes
##########################################################################

class BaseConsumer(LoggableMixin):
    """Base consumer class"""

    def __init__(self, *args, **kwargs):
        self.ready = False
        super(BaseConsumer, self).__init__(*args, **kwargs)

    def setup(self, *args, **kwargs):
        self.ready = True

    def send(self, *args, **kwargs):
        raise NotImplementedError()

    def listen(self, *args, **kwargs):
        raise NotImplementedError()

    def shutdown(self, *args, **kwargs):
        self.logger.info("{}: shutdown complete".format(self.__class__.__name__))


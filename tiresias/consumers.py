# tiresias.consumers
# module description
#
# Author:   Allen Leis <allen.leis@gmail.com>
# Created:  Tue Apr 16 19:39:10 2019 -0400
#
# Copyright (C) 2017 Allen Leis
# For license information, see LICENSE
#
# ID: consumers.py [] allen.leis@gmail.com $

"""
module description
"""

##########################################################################
# Imports
##########################################################################

import json

from tiresias.utils.logger import LoggableMixin

##########################################################################
# Classes
##########################################################################

class BaseConsumer(LoggableMixin):

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


class JSONConsumer(BaseConsumer):

    def __init__(self, filename="data.json", *args, **kwargs):
        self.filename = filename
        super(JSONConsumer, self).__init__(*args, **kwargs)

    def setup(self, *args, **kwargs):
        self.file = open(self.filename, "w")
        self.logger.info("JSONConsumer: opening file `{}`".format(self.filename))
        super(JSONConsumer, self).setup(*args, **kwargs)

    def send(self, data):
        if not self.ready:
            raise RuntimeError("JSONConsumer: send attempted but instance not configured")
        self.file.write(json.dumps(data) + "\n")

    def listen(self, queue):
        try:
            while True:
                item = queue.get()
                if item is None:
                    self.logger.info("JSONConsumer: exiting listen mode")
                    break
                self.send(item)

        except KeyboardInterrupt:
            pass

        self.shutdown()

    def shutdown(self, *args, **kwargs):
        self.logger.info("JSONConsumer: closing file `{}`".format(self.filename))
        self.file.close()
        super(JSONConsumer, self).__init__(*args, **kwargs)


##########################################################################
# Execution
##########################################################################

if __name__ == '__main__':
    pass
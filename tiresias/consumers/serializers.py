# tiresias.consumers.serializers
# Consumers that save data to disk
#
# Author:   Allen Leis <allen.leis@gmail.com>
# Created:  Tue Apr 16 19:39:10 2019 -0400
#
# Copyright (C) 2017 Allen Leis
# For license information, see LICENSE
#
# ID: serializers.py [] allen.leis@gmail.com $

"""
Consumers that save data to disk
"""

##########################################################################
# Imports
##########################################################################

import os
import json
import datetime

from tiresias.consumers.base import BaseConsumer

RESET_CMD = "RESET_CMD"
TRASH_CMD = "TRASH_CMD"

##########################################################################
# Classes
##########################################################################

class JSONConsumer(BaseConsumer):
    """Writes data to a JSON file"""

    target_directory = "data"

    def __init__(self, filename="data_{}.json", *args, **kwargs):
        self.filename_template = filename
        if not os.path.exists(self.target_directory):
            os.makedirs(self.target_directory)
        super(JSONConsumer, self).__init__(*args, **kwargs)

    @property
    def filename(self):
        dt = datetime.datetime.now().strftime("%F-%H%M%S")
        filename = self.filename_template.format(dt)
        return os.path.join(self.target_directory, filename)

    def setup(self, *args, **kwargs):
        self.file = open(self.filename, "w")
        self.logger.info("JSONConsumer: opening file `{}`".format(self.filename))
        super(JSONConsumer, self).setup(*args, **kwargs)

    def reset(self, *args, **kwargs):
        self.logger.info("JSONConsumer: closing file")
        self.file.close()
        self.setup()

    def trash(self, *args, **kwargs):
        self.logger.info("JSONConsumer: trashing file")
        self.file.close()
        os.remove(self.file.name)
        self.setup()

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

                if item is RESET_CMD:
                    self.logger.info("JSONConsumer: RESET received")
                    self.reset()

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

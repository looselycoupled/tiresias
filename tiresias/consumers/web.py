# tiresias.consumers.web
# Consumers to render sensor data in a website
#
# Author:   Allen Leis <allen.leis@gmail.com>
# Created:  Tue Apr 16 19:39:10 2019 -0400
#
# Copyright (C) 2017 Allen Leis
# For license information, see LICENSE
#
# ID: web.py [] allen.leis@gmail.com $

"""
Consumers to render sensor data in a website
"""

##########################################################################
# Imports
##########################################################################

import json
import time

import threading
import random


from flask import Flask, render_template
from flask_socketio import SocketIO

from tiresias.consumers.base import BaseConsumer

sensor_data_changed = threading.Condition()
sensor_data = {}

##########################################################################
# Flask
##########################################################################

app = Flask(__name__)
app.config['SECRET_KEY'] = '4949f8f5beb339df992906c4218714e4#'
socketio = SocketIO(app)
active_connections = 0

##########################################################################
# Classes
##########################################################################

class FlaskConsumer(BaseConsumer):
    """Real time web application to view sensor data"""

    def __init__(self, *args, **kwargs):
        self.thread = None
        super(FlaskConsumer, self).__init__(*args, **kwargs)

    def setup(self, *args, **kwargs):
        super(FlaskConsumer, self).setup(*args, **kwargs)

    def send(self, data):
        raise NotImplementedError()

    @app.route('/')
    def render_index():
        return render_template('index.html')

    @socketio.on('connect')
    def handle_connect():
        global active_connections
        # print("connection detected")
        active_connections += 1

    @socketio.on('disconnect')
    def handle_disconnect():
        global active_connections
        # print('Client disconnected')
        active_connections -= 1

    def read_queue(self, queue):
        global sensor_data
        global socketio

        while True:
            sensor_data = queue.get()
            with sensor_data_changed:

                # Notify any waiting threads
                sensor_data_changed.notifyAll()

                if active_connections > 0:
                    socketio.emit('update', sensor_data)


    def listen(self, queue):

        self.thread = threading.Thread(target=self.read_queue, args=(queue, ))
        self.thread.daemon = True
        self.thread.start()

        socketio.run(app, host="0.0.0.0", debug=True)

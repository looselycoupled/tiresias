import time
from tiresias.utils.logger import LoggableMixin

# For Demo
import os
import threading
from flask import Flask, render_template, request, send_from_directory
from flask_socketio import SocketIO

SAMPLE_LOGGING_INTERVAL = 100
SAMPLE_DURATION = 0.0096

##########################################################################
# Flask
##########################################################################

app = Flask(__name__, template_folder="consumers/templates", static_url_path="/static", static_folder="./consumers/templates/static")
app.config['SECRET_KEY'] = '4949f8f5beb339df992906c4218714e4#'
socketio = SocketIO(app)
thread = None

@app.route('/')
def render_index():
    return render_template('index.html')


class FlaskManager(LoggableMixin):

    def __init__(self, sensors, consumers):
        self.sensors = sensors
        self.consumers = consumers
        super(FlaskManager, self).__init__()

    def _setup(self):
        for s in self.sensors:
            s.setup()
        for c in self.consumers:
            c.setup()

    def start(self):
        global thread
        global socketio
        global app

        self._setup()

        thread = threading.Thread(target=socketio.run, args=(app, ), kwargs={"host": "0.0.0.0", "debug": False})
        thread.daemon = True
        thread.start()

        try:

            while True:
                start = time.time()
                data = {"time": { "start": int(start * 1e6), "scale": "microsecond"}}

                for s in self.sensors:
                    data.update(s.read())
                    if hasattr(s, "status"):
                        data.update(s.status())

                socketio.emit('update', data)
                time.sleep(.05)

        except KeyboardInterrupt:
            self.logger.info("Manager: exit requested")

    def end(self):
        pass
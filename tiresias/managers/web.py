import time
from tiresias.utils.logger import LoggableMixin

# For Demo
import os
import threading
from flask import Flask, render_template, request, send_from_directory, jsonify
from flask_socketio import SocketIO

SAMPLE_LOGGING_INTERVAL = 100
SAMPLE_DURATION = 0.0096

RESET_CMD = "RESET_CMD" # start new data ingest
TRASH_CMD = "TRASH_CMD" # throw away data ingest

##########################################################################
# Flask
##########################################################################

app = Flask(
    __name__,
    template_folder="../consumers/templates",
    static_url_path="/static",
    static_folder="../consumers/templates/static"
)
app.config['SECRET_KEY'] = '4949f8f5beb339df992906c4218714e4#'
socketio = SocketIO(app)
thread = None
client_command = None


@app.route('/')
def render_index():
    return render_template('index.html')

@app.route('/reset', methods=['POST'])
def handle_consumer_reset():
    global client_command
    client_command = RESET_CMD
    return jsonify({})

@app.route('/trash', methods=['POST'])
def handle_consumer_trash():
    global client_command
    client_command = TRASH_CMD
    return jsonify({})



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
        global client_command

        self._setup()

        thread = threading.Thread(target=socketio.run, args=(app, ), kwargs={"host": "0.0.0.0", "debug": False})
        thread.daemon = True
        thread.start()

        try:
            rate = {"start": time.time(), "samples": 0}
            while True:
                start = time.time()
                data = {"time": { "start": int(start * 1e6), "scale": "microsecond"}}

                # read data from sensors
                for s in self.sensors:
                    data.update(s.read())
                    if hasattr(s, "status"):
                        data.update(s.status())

                # send data to consumers
                for c in self.consumers:
                    c.send(data)

                    # send special command to consumer if requested
                    if client_command == RESET_CMD:
                        if hasattr(c, "reset"):
                            c.reset()
                    if client_command == TRASH_CMD:
                        if hasattr(c, "trash"):
                            c.trash()

                socketio.emit('update', data)
                client_command = None

                # keep track of samples per second
                rate["samples"] += 1
                if time.time() - rate["start"] > 1:
                    self.logger.info("Manager: {} samples per second".format(rate["samples"]))
                    rate = {"start": time.time(), "samples": 0}

                # .0064 gets you about 50Hz
                time.sleep(.0064)

        except KeyboardInterrupt:
            self.logger.info("Manager: exit requested")

    def end(self):
        pass

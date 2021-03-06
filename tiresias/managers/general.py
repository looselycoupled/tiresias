import time
import multiprocessing as mp
from tiresias.utils.logger import LoggableMixin


SAMPLE_LOGGING_INTERVAL = 100
SAMPLE_DURATION = 0.0096

class Manager(LoggableMixin):

    def __init__(self, sensors, consumers):
        self.sensors = sensors
        self.consumers = consumers
        super(Manager, self).__init__()

    def _setup(self):
        for s in self.sensors:
            s.setup()
        for c in self.consumers:
            c.setup()

    def start(self):
        counter = 0
        command_queues = [mp.Queue() for _ in self.sensors]
        consumer_queues = [mp.Queue() for _ in self.consumers]
        output = mp.Queue()
        self._setup()

        try:
            procs = [
                mp.Process(name=s.__class__.__name__, target=s.monitor, args=(command_queues[idx], output), daemon=False)
                for idx, s in enumerate(self.sensors)
            ]
            procs += [
                mp.Process(name=c.__class__.__name__, target=c.listen, args=(consumer_queues[idx],))
                for idx, c in enumerate(self.consumers)
            ]
            for p in procs:
                p.start()

            while True:
                start = time.time()
                data = {"time": { "start": int(start * 1e6), "scale": "microsecond"}}

                for q in command_queues:
                    q.put(True)

                for _ in self.sensors:
                    data.update(output.get())

                duration = time.time() - start
                data["time"].update({"duration": int(duration * 1e6)})

                for q in consumer_queues:
                    q.put(data)

                counter += 1
                if counter % SAMPLE_LOGGING_INTERVAL == 0:
                    self.logger.info("Manager: {} samples processed, {:,} total".format(SAMPLE_LOGGING_INTERVAL, counter))

                # try to sleep such that samples are near SAMPLE_DURATION apart
                time.sleep(max(SAMPLE_DURATION - duration, 0))

        except KeyboardInterrupt:
            self.logger.info("Manager: exit requested")
            for q in command_queues:
                q.put(None)
            for p in procs:
                p.join()
            self.logger.info("Manager: exiting")

    def end(self):
        pass

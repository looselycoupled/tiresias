import time
import multiprocessing as mp
from tiresias.utils.logger import LoggableMixin

class Manager(LoggableMixin):

    def __init__(self, sensors, consumers):
        self.sensors = sensors
        self.consumers = consumers
        super(Manager, self).__init__()

    def _setup(self):
        for s in self.sensors:
            s.setup()

    def start(self):
        command_queues = [mp.Queue() for _ in self.sensors]
        output = mp.Queue()
        self._setup()

        try:
            procs = [
                mp.Process(name=s.__class__.__name__, target=s.monitor, args=(command_queues[idx], output), daemon=False)
                for idx, s in enumerate(self.sensors)
            ]
            for p in procs:
                p.start()

            while True:
                start = time.time()
                data = {"time": { "start": int(start * 1e6), "scale": "microsecond"}}

                for q in command_queues:
                    q.put(True)

                for _ in procs:
                    data.update(output.get())

                data["time"].update({"duration": time.time() - start})
                print(data)
                time.sleep(.01)


        except KeyboardInterrupt:
            self.logger.info("Manager: exit requested")
            for q in command_queues:
                q.put(None)
            for p in procs:
                p.join()
            self.logger.info("Manager: exiting")

    def end(self):
        pass

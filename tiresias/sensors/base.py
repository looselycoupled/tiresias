from tiresias.utils.logger import LoggableMixin

class SensorBase(LoggableMixin):

    def __init__(self, *args, **kwargs):
        self._ready = False
        super(SensorBase, self).__init__(*args, **kwargs)

    def setup(self):
        self._ready = True

    def shutdown(self):
        pass

    def read(self):
        raise NotImplementedError()

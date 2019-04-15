from tiresias.utils.logger import LoggableMixin

class SensorBase(LoggableMixin):

    def __init__(self, *args, **kwargs):
        self._configured = False
        super(SensorBase, self).__init__(*args, **kwargs)

    def setup(self):
        self._configured = True

    def shutdown(self):
        pass

    def read(self):
        raise NotImplementedError()

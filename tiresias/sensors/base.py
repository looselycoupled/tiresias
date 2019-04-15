from tiresias.utils.logging import LoggableMixin

class SensorBase(LoggableMixin):

    def __init__(self, *args, **kwargs):
        self._configured = False

    def setup(self):
        self._configured = True

    def teardown(self):
        pass


    def read(self):
        raise NotImplementedError()
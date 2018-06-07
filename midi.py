from Mido import message

class MockMidiIn(object):
    """docstring for MockMidiIn."""
    def __init__(self, arg):
        super(MockMidiIn, self).__init__()
        self.arg = arg

    def iter_pending(self):
        for i in range(100):
            yield message(type='clock')


class MockMidiOut(object):
    """docstring for MockMidiIn."""
    def __init__(self, arg):
        super(MockMidiIn, self).__init__()
        self.arg = arg

    def send(self, msg):
        self.buffer.append(msg)

    def get_output(self):
        return self.buffer

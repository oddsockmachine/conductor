from mido import Message

class MockMidiIn(object):
    """docstring for MockMidiIn."""
    def __init__(self):
        super(MockMidiIn, self).__init__()
        self.total = 100
        self.count = 0

    def iter_pending(self):
        # yield Message(type='start_pos')
        if self.count < self.total:
            for i in range(10):
                self.count += 1
                yield Message(type='clock')

class MockMidiOut(object):
    """docstring for MockMidiIn."""
    def __init__(self, arg):
        super(MockMidiIn, self).__init__()
        self.arg = arg

    def send(self, msg):
        self.buffer.append(msg)

    def get_output(self):
        return self.buffer

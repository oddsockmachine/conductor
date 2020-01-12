from threading import Thread
from constants import debug

class MidiOut(Thread):
    """Listen to MIDI queue, send msgs out thru bus"""
    def __init__(self, mportout, midi_out_bus):
        Thread.__init__(self, name='MidiOutput')
        self.daemon = True
        self.mportout = mportout
        self.midi_out_bus = midi_out_bus

    def run(self):
        debug("MidiOut")
        while True:
            msgs = self.midi_out_bus.get()
            for msg in msgs:
                self.mportout.send(msg)
                # debug(msg)
        return

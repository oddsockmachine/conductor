from threading import Thread
from constants import debug
from buses import bus_registry

class MidiOut(Thread):
    """Listen to MIDI queue, send msgs out thru bus"""
    def __init__(self, mportout):
        Thread.__init__(self, name='MidiOutput')
        self.daemon = True
        self.mportout = mportout
        self.midi_out_bus = bus_registry.get('midi_out_bus')
        self.keep_running = True

    def run(self):
        debug("MidiOut starting")
        while self.keep_running:
            msgs = self.midi_out_bus.get()
            for msg in msgs:
                self.mportout.send(msg)
                # debug(msg)
        return

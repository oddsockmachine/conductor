from threading import Thread
from constants import debug, TICK, BEAT
from time import sleep
from random import randint
from queue import Queue

class MidiOut(Thread):
    """Listen to MIDI queue, send msgs out thru bus"""
    def __init__(self, mportout, midi_out_bus):
        Thread.__init__(self, name='MidiInListener')
        self.mportout = mportout
        self.midi_out_bus = midi_out_bus

    def run(self):
        debug("MidiOut")
        while True:
            sleep(1)
            note = self.midi_out_bus.get()
            self.mportout.send(note)
        return

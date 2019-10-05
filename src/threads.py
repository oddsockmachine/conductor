import threading
from constants import debug
from time import sleep
from random import randint
from queue import Queue
from mido import open_input
from buses import midi_in_bus, LEDs_bus, buttons_bus, clock_bus, ticker_bus
from midi_input import MidiInListener
from clock import Clock
from ticker import SelfTicker


mportin = open_input('SuperCell_In', autoreset=True, virtual=True)
midi = MidiInListener(mportin, midi_in_bus)
ticker = SelfTicker(100, ticker_bus)
clock = Clock(midi_in_bus, ticker_bus, clock_bus)

midi.start()
ticker.start()
clock.start()
clock.set_input("tick")
while True:
    if not clock_bus.empty():
        print(clock_bus.get())
    sleep(0.01)
    # clock.set_input("midi") if randint(0,1000)>990 else clock.set_input("tick")






class Instrument(threading.Thread):
    """Listen on both midi and ticker clock buses, pass through clock messages based on chosen input"""
    def __init__(self, midi_in_bus, ticker_bus, clock_bus):
        threading.Thread.__init__(self, name='Instrument')
        self.q = Queue()  # Internal queue for communications

    def communicate(self, msg):
        self.q.put(msg)


    def run(self):
        return

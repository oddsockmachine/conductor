from threading import Thread
from constants import debug, TICK, BEAT

class Clock(Thread):
    """Listen on both midi and ticker clock buses, pass through clock messages based on chosen input"""
    def __init__(self, midi_in_bus, ticker_bus, clock_bus):
        Thread.__init__(self, name='Clock')
        self.input = "midi"
        self.ticker_bus = ticker_bus
        self.midi_in_bus = midi_in_bus
        self.clock_bus = clock_bus

    def set_input(self, inp):
        if inp == self.input:
            return
        debug(f"Changing clock input to {inp}")
        # self.midi_in_bus.clear()
        # self.ticker_bus.clear()
        self.input = inp
        return

    def run(self):
        debug("foo")
        while True:
            if self.input == "midi":
                # if not self.midi_in_bus.empty():
                    # debug("ok")
                x = self.midi_in_bus.get()
                    # debug("midi")
                self.clock_bus.put(x)
            else:
                # if not self.ticker_bus.empty():
                    # debug("ok")
                x= self.ticker_bus.get()
                    # debug("tick")
                self.clock_bus.put(x)
        return


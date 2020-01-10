from threading import Thread
from constants import debug, TICK, BEAT

class Clock(Thread):
    """Listen on both midi and ticker clock buses, pass through clock messages based on chosen input"""
    def __init__(self, midi_in_bus, ticker_bus, clock_bus, inp):
        Thread.__init__(self, name='Clock')
        self.daemon = True
        self.input = inp
        debug("Clock input is " + str(inp))
        self.ticker_bus = ticker_bus
        self.midi_in_bus = midi_in_bus
        self.clock_bus = clock_bus

    def run(self):
        debug("foo")
        while True:
            if self.input == "midi":
                x = self.midi_in_bus.get()
                self.clock_bus.put(x)
            else:
                x = self.ticker_bus.get()
                self.clock_bus.put(x)
        return

    def set_input(self, inp):
        # TODO maybe delete this, no need to change inputs mid-set
        if inp == self.input:
            return
        debug("Changing clock input to " + inp)
        self.input = inp
        self.midi_in_bus.queue.clear()
        self.ticker_bus.queue.clear()
        return

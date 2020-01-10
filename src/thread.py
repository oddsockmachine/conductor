from threading import Thread
from time import sleep
from constants import debug, TICK, BEAT

class Proc(Thread):
    """Automatically generate clock pulses at the required BPM"""
    def __init__(self, name, bus_list, router):
        Thread.__init__(self, name=name)
        self.daemon = True
        self.ticker_bus = bus_list[0]

    def run(self):
        debug(f"{self.name} started")
        while True:
            sleep(0.01)
            # Wait/get
            self.ticker_bus.put("tick")

        return

    def send(self, bus, msg):
        return
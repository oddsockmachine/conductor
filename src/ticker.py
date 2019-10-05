from threading import Thread
from time import sleep
from constants import debug, TICK, BEAT

class SelfTicker(Thread):
    """Automatically generate clock pulses at the required BPM"""
    def __init__(self, initial_bpm, ticker_bus):
        Thread.__init__(self, name='SelfTicker')
        self.bpm = initial_bpm
        self.ticker_bus = ticker_bus
        self.beat_clock_count = 0
        self.midi_clock_divider = 12

    def run(self):
        debug("SelfTicker")
        while True:
            sleep(60/self.bpm)
            debug("tick in")
            self.ticker_bus.put("x")
        tick = self.process_midi_tick()
        self.ticker_bus.put(tick)

        return

    def process_midi_tick(self):
        '''Perform midi tick subdivision so ticks only happen on beats'''
        self.beat_clock_count += 1
        if self.beat_clock_count >= self.midi_clock_divider:
            self.beat_clock_count %= self.midi_clock_divider
            print(".")
            return BEAT
        return TICK
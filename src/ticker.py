from threading import Thread
from time import sleep
from constants import debug, TICK, BEAT
from mido import Message
from buses import bus_registry

class SelfTicker(Thread):
    """Automatically generate clock pulses at the required BPM"""
    def __init__(self, initial_bpm):
        Thread.__init__(self, name='SelfTicker')
        self.daemon = True
        self.bpm = initial_bpm
        if initial_bpm:
            debug("ticker's bpm is " + str(initial_bpm))
        self.ticker_bus = bus_registry.get('ticker_bus')
        self.beat_clock_count = 0
        self.midi_clock_divider = 32
        self.midi_out_bus = bus_registry.get('midi_out_bus')
        self.keep_running = True

    def run(self):
        if not self.bpm:
            debug("Not using self ticker")
            return
        debug("SelfTicker started")
        sleep_period = 60/self.bpm
        while self.keep_running:
            sleep(sleep_period)
            tick = self.process_midi_tick()
            self.ticker_bus.put(tick)
            if self.midi_out_bus:
                self.midi_out_bus.put([Message('clock')])
        return

    def process_midi_tick(self):
        '''Perform midi tick subdivision so ticks only happen on beats'''
        self.beat_clock_count += 1
        if self.beat_clock_count >= self.midi_clock_divider:
            self.beat_clock_count %= self.midi_clock_divider
            return BEAT
        return TICK
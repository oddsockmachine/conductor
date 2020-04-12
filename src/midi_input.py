from threading import Thread
from constants import debug, TICK, BEAT
from time import sleep
from random import randint
from buses import bus_registry

class MidiInListener(Thread):
    """Listen on MIDI in port. Clock msgs go to clock bus, note msgs go to note bus"""
    def __init__(self, mportin):
        Thread.__init__(self, name='MidiInListener')
        self.daemon = True
        self.mportin = mportin
        self.midi_in_bus = bus_registry.get('midi_in_bus')
        self.clock_count = 0
        self.beat_count = 0
        self.midi_clock_divider = 3
        # self.midi_beat_divider = 3
        self.count = 0
        self.keep_running = True

    def run(self):
        self.mportin.callback = self.process_incoming_midi()
        debug("MidiInListener starting")
        while self.keep_running:
            # beat = randint(110,120)
            # debug("midi still running")
            sleep(1)
            # self.midi_in_bus.put("x")
        return

    def process_incoming_midi(self):
        def _process_incoming_midi(message):
            '''Check for incoming midi messages and categorize so we can do something with them'''
            if message.type == "clock":
                self.count += 1
                self.count %= 24
                debug(self.count)
                tick = self.process_midi_tick()
                self.midi_in_bus.put(tick)

        return _process_incoming_midi

    def process_midi_tick(self):
        '''Perform midi tick subdivision so ticks only happen on beats'''
        # self.beat_count += 1
        # if self.beat_count >= self.midi_beat_divider:
        self.clock_count += 1
    
        if self.clock_count >= self.midi_clock_divider:
            self.clock_count %= self.midi_clock_divider
            debug("----------------------")
            return BEAT
        debug("---")
        return TICK
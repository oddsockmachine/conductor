import mido
from midi_input import MidiInListener
from time import sleep
from buses import bus_registry
from constants import BEAT, TICK
with mido.open_input('supervisor_In', autoreset=True, virtual=True) as mportin:
    counter = 0
    midi_in = MidiInListener(mportin)
    midi_in.start()
    midi_in_bus = bus_registry.get('midi_in_bus')
    while True:
        msg = midi_in_bus.get()
        couunter += 1
        print(counter)
        if msg == BEAT:
            print('----')
        if msg == TICK:
            print('x')
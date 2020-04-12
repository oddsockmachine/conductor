import mido
from src.midi_input import MidiInListener
from time import sleep

with mido.open_input('supervisor_In', autoreset=True, virtual=True) as mportin:
    midi_in = MidiInListener(mportin)
    midi_in.start()
    sleep(100)
from instruments.instrument import Instrument
# from instruments.beatmaker import BeatMaker
# from instruments.binary_sequencer import BinarySequencer
# from instruments.chord_sequencer import ChordSequencer
from instruments.droplets import Droplets
from instruments.drum_big import DrumBig
# from instruments.drum_deviator import DrumDeviator
from instruments.drum_machine import DrumMachine
# from instruments.elaborator import Elaborator
from instruments.euclidean_generator import Euclidean
from instruments.octopus import Octopus
from instruments.sequencer import Sequencer
# from instruments.transformer import Transformer
from instruments.cc import CC
from instruments.keyboard import Keyboard

instrument_lookup_data = {
    0: Instrument,  # Generic, fallback, no functionality
    # 1: BeatMaker,
    # 2: BinarySequencer,
    # 3: ChordSequencer,
    1: Droplets,
    2: DrumBig,
    # 5: DrumDeviator
    3: DrumMachine,
    # 7: Elaborator,
    4: Euclidean,
    5: Octopus,
    6: Sequencer,
    # 11: Transformer,
    7: CC,
    8: Keyboard,
    'Instrument': Instrument,  # Generic, fallback, no functionality
    # 'BeatMaker': BeatMaker,
    # 'BinarySequencer': BinarySequencer,
    # 'ChordSequencer': ChordSequencer,
    'Droplets': Droplets,
    'DrumBig': DrumBig,
    # 'DrumDeviator': DrumDeviator,
    'DrumMachine': DrumMachine,
    # 'Elaborator': Elaborator,
    'Euclidean': Euclidean,
    'Octopus': Octopus,
    'Sequencer': Sequencer,
    # 'Transformer': Transformer,
    'CC': CC,
    'Keyboard': Keyboard,
}


def instrument_lookup(num):
    return instrument_lookup_data[num]

from instruments.instrument import Instrument
from instruments.beatmaker import BeatMaker
from instruments.binary_sequencer import BinarySequencer
from instruments.chord_sequencer import ChordSequencer
from instruments.droplets import Droplets
from instruments.drum_big import DrumBig
# from instruments.drum_deviator import DrumDeviator
from instruments.drum_machine import DrumMachine
from instruments.elaborator import Elaborator
from instruments.euclidean_generator import Euclidean
from instruments.octopus import Octopus
from instruments.sequencer import Sequencer
from instruments.transformer import Transformer
from instruments.cc import CC
from instruments.keyboard import Keyboard


def instrument_lookup(num):
    return {
        0: Instrument,  # Generic, fallback, no functionality
        1: BeatMaker,
        2: BinarySequencer,
        3: ChordSequencer,
        4: Droplets,
        5: DrumBig,
        # 5: DrumDeviator
        6: DrumMachine,
        7: Elaborator,
        8: Euclidean,
        9: Octopus,
        10: Sequencer,
        11: Transformer,
        12: CC,
        14: Keyboard,
        'Instrument': Instrument,  # Generic, fallback, no functionality
        'BeatMaker': BeatMaker,
        'BinarySequencer': BinarySequencer,
        'ChordSequencer': ChordSequencer,
        'Droplets': Droplets,
        'DrumBig': DrumBig,
        # 'DrumDeviator': DrumDeviator,
        'DrumMachine': DrumMachine,
        'Elaborator': Elaborator,
        'Euclidean': Euclidean,
        'Octopus': Octopus,
        'Sequencer': Sequencer,
        'Transformer': Transformer,
        'CC': CC,
        'Keyboard': Keyboard,
    }[num]

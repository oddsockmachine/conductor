from supercell import Supercell
import mido
import argparse
from buses import midi_in_bus, midi_out_bus, LEDs_bus, buttons_bus, clock_bus, ticker_bus
from midi_input import MidiInListener
from midi_output import MidiOut
from clock import Clock
from ticker import SelfTicker
from constants import debug

parser = argparse.ArgumentParser()
parser.add_argument("--hw",  help="Use real hardware", type=bool)
parser.add_argument("--bpm",  help="Use real hardware", type=int)
args = parser.parse_args()
debug(args)
bpm = int(args.bpm) if args.bpm else None


def console_main(stdscr):
    from interfaces.console import Display
    curses.mousemask(1)
    curses.mouseinterval(10)
    stdscr.nodelay(1)
    display = Display(stdscr, buttons_bus, LEDs_bus)
    with mido.open_output('SuperCell_Out', autoreset=True, virtual=True) as mportout:
        with mido.open_input('SuperCell_In', autoreset=True, virtual=True) as mportin:
            start_supercell(display, mportin, mportout, midi_in_bus, midi_out_bus, ticker_bus, clock_bus, bpm)


def hardware_main():
    from interfaces.hardware import Display
    display = Display(buttons_bus, LEDs_bus)
    debug(mido.get_input_names())
    debug(mido.get_output_names())
    debug("Creating MIDI ports")
    with mido.open_output('f_midi:f_midi 16:0') as mportout:
        with mido.open_input('f_midi:f_midi 16:0') as mportin:
            start_supercell(display, mportin, mportout, midi_in_bus, midi_out_bus, ticker_bus, clock_bus, bpm)


def start_supercell(display, mportin, mportout, midi_in_bus, midi_out_bus, ticker_bus, clock_bus, bpm):
    midi_in = MidiInListener(mportin, midi_in_bus)
    midi_out = MidiOut(mportout, midi_out_bus)
    ticker = SelfTicker(bpm, ticker_bus)
    clock = Clock(midi_in_bus, ticker_bus, clock_bus, 'tick' if bpm else 'midi')
    midi_in.start()
    midi_out.start()
    ticker.start()
    clock.start()
    display.start()
    supercell = Supercell(clock_bus, buttons_bus, LEDs_bus)
    supercell.run()


if __name__ == '__main__':
    if not args.hw:
        import curses
        curses.wrapper(console_main)
    else:
        hardware_main()

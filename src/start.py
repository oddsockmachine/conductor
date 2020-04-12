from supervisor import Supervisor
import mido
import argparse
from buses import midi_in_bus, midi_out_bus, LED_grid_bus, button_grid_bus, clock_bus, ticker_bus
from midi_input import MidiInListener
from midi_output import MidiOut
from clock import Clock
from ticker import SelfTicker
from constants import debug
# import atexit

parser = argparse.ArgumentParser()
parser.add_argument("--hw",  help="Use real hardware", type=bool)
parser.add_argument("--bpm",  help="Use real hardware", type=int)
args = parser.parse_args()
debug(args)
bpm = int(args.bpm) if args.bpm else None


def console_main(stdscr):
    from interfaces.console import Display
    from interfaces.oled_sw import OLED_Screens
    OLED_Screens = OLED_Screens.start(4)
    curses.mousemask(1)
    curses.mouseinterval(10)
    curses.curs_set(0)
    stdscr.nodelay(1)
    display = Display(stdscr)
    with mido.open_output('supervisor_Out', autoreset=True, virtual=True) as mportout:
        with mido.open_input('supervisor_In', autoreset=True, virtual=True) as mportin:
            start_supervisor(display, mportin, mportout, bpm)


def hardware_main():
    from interfaces.hardware import Display
    from interfaces.oled_hw import OLED_Screens

    # from interfaces.encoders import Encoder_Inputs, Encoder_RGB
    from interfaces.i2c_bus import i2c_bus
    # TODO create  i2c bus here, pass to Display
    display = Display(i2c_bus)
    # encoders = Encoder_Inputs(encoder_out_bus, button_grid_bus, i2c_bus)
    # encoders.start()
    # encoders_RGB = Encoder_RGB(encoder_in_bus, i2c_bus)
    # encoders_RGB.start()
    debug(mido.get_input_names())
    debug(mido.get_output_names())
    debug("Creating MIDI ports")
    with mido.open_output('f_midi:f_midi 16:0') as mportout:
        with mido.open_input('f_midi:f_midi 16:0') as mportin:
            start_supervisor(display, mportin, mportout, bpm)


def start_supervisor(display, mportin, mportout, bpm):
    midi_in = MidiInListener(mportin)
    midi_out = MidiOut(mportout)
    ticker = SelfTicker(bpm)
    clock = Clock('tick' if bpm else 'midi')
    midi_in.start()
    midi_out.start()
    ticker.start()
    clock.start()
    display.start()
    supervisor = Supervisor()
    try:
        supervisor.run()
    finally:
        debug("Stopping everything")
        midi_in.keep_running = False
        midi_out.keep_running = False
        ticker.keep_running = False
        clock.keep_running = False
        display.keep_running = False
        supervisor.keep_running = False
        debug("Threads stopped")
        exit()
        debug("exiting?")

if __name__ == '__main__':
    if not args.hw:
        import curses
        curses.wrapper(console_main)
    else:
        hardware_main()

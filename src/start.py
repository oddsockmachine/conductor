from supervisor import Supervisor
import mido
import argparse
from buses import midi_in_bus, midi_out_bus, LEDs_bus, buttons_bus, clock_bus, ticker_bus, encoder_in_bus, encoder_out_bus, button_out_bus
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
    from interfaces.oled import OLED_Screens
    OLED_Screens = OLED_Screens.start(4).proxy()
    curses.mousemask(1)
    curses.mouseinterval(10)
    curses.curs_set(0)
    stdscr.nodelay(1)
    display = Display(stdscr, buttons_bus, LEDs_bus, OLED_Screens)
    with mido.open_output('supervisor_Out', autoreset=True, virtual=True) as mportout:
        with mido.open_input('supervisor_In', autoreset=True, virtual=True) as mportin:
            start_supervisor(display, mportin, mportout, midi_in_bus, midi_out_bus, ticker_bus, clock_bus, bpm)


def hardware_main():
    from interfaces.hardware import Display
    from interfaces.encoders import Encoder_Inputs, Encoder_RGB
    from interfaces.i2c_bus import i2c_bus
    # TODO create  i2c bus here, pass to Display
    display = Display(buttons_bus, LEDs_bus, i2c_bus)
    encoders = Encoder_Inputs(encoder_out_bus, button_out_bus, i2c_bus)
    encoders.start()
    encoders_RGB = Encoder_RGB(encoder_in_bus, i2c_bus)
    encoders_RGB.start()
    debug(mido.get_input_names())
    debug(mido.get_output_names())
    debug("Creating MIDI ports")
    with mido.open_output('f_midi:f_midi 16:0') as mportout:
        with mido.open_input('f_midi:f_midi 16:0') as mportin:
            start_supervisor(display, mportin, mportout, midi_in_bus, midi_out_bus, ticker_bus, clock_bus, bpm)


def start_supervisor(display, mportin, mportout, midi_in_bus, midi_out_bus, ticker_bus, clock_bus, bpm):
    midi_in = MidiInListener(mportin, midi_in_bus)
    midi_out = MidiOut(mportout, midi_out_bus)
    ticker = SelfTicker(bpm, ticker_bus, midi_out_bus)
    clock = Clock(midi_in_bus, ticker_bus, clock_bus, 'tick' if bpm else 'midi')
    midi_in.start()
    midi_out.start()
    ticker.start()
    clock.start()
    display.start()
    supervisor = Supervisor(clock_bus, buttons_bus, LEDs_bus)
    supervisor.run()


if __name__ == '__main__':
    if not args.hw:
        import curses
        curses.wrapper(console_main)
    else:
        hardware_main()

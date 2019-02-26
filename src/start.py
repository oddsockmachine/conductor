from supercell import Supercell
import mido
import argparse

# Get command line arguments, set up midi connections, start up Supercell in correct mode

parser = argparse.ArgumentParser()
parser.add_argument("--set", help="Filename of previous set to load", type=str)
parser.add_argument("--hw",  help="Use real hardware", type=bool)
args = parser.parse_args()
print(args)

def console_main(stdscr):
    from interfaces.console import Display
    m = curses.mousemask(1)
    curses.mouseinterval(10)
    stdscr.nodelay(1)
    display = Display(stdscr)
    with mido.open_output('SuperCell_Out', autoreset=True, virtual=True) as mport:
        with mido.open_input('SuperCell_In', autoreset=True, virtual=True) as mportin:
            supercell = Supercell(display, mport, mportin, args.set)
            supercell.run()

def hardware_main():
    from interfaces.hardware import Display
    display = Display()
    print(mido.get_input_names())
    print(mido.get_output_names())
    with mido.open_output('f_midi:f_midi 16:0') as mport:
        with mido.open_input('f_midi:f_midi 16:0') as mportin:
            print(mportin)
            print(mport)
            supercell = Supercell(display, mport, mportin, args.set)
            supercell.sequencer.instruments[0].add_page(0)
            supercell.sequencer.instruments[0].add_page(1)
            supercell.sequencer.instruments[0].add_page(1)
            supercell.sequencer.instruments[0].inc_page_repeats(0)
            supercell.sequencer.instruments[0].inc_page_repeats(0)
            supercell.sequencer.instruments[0].add_page(1)
            supercell.sequencer.instruments[0].inc_page_repeats(1)
            supercell.sequencer.instruments[0].inc_page_repeats(0)
            supercell.sequencer.instruments[3].add_page(1)
            supercell.sequencer.instruments[3].add_page(1)
            supercell.sequencer.instruments[3].inc_page_repeats(0)
            supercell.sequencer.instruments[6].add_page(1)
            supercell.run()

if __name__ == '__main__':
    if not args.hw:
        import curses
        curses.wrapper(console_main)
    else:
        hardware_main()

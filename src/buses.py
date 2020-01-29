from queue import Queue

midi_in_bus = Queue(100)
midi_out_bus = Queue(200)
encoder_in_bus = Queue(200)
encoder_out_bus = Queue(100)
OLED_bus = Queue(100)
ticker_bus = Queue(100)
clock_bus = Queue(100)
buttons_bus = Queue()
button_out_bus = Queue()
LEDs_bus = Queue()

def clear_queue(q):
    while not q.empty():
        q.get()
    return

def all_buses():
    return {
        'midi_in_bus': midi_in_bus,
        'midi_out_bus': midi_out_bus,
        'ticker_bus': ticker_bus,
        'clock_bus': clock_bus,
        'buttons_bus': buttons_bus,
        'LEDs_bus': LEDs_bus, 
    }

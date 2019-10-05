from queue import Queue

midi_in_bus = Queue(100)
ticker_bus = Queue(100)
clock_bus = Queue(100)
buttons_bus = Queue()
LEDs_bus = Queue()

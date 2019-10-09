from queue import Queue

midi_in_bus = Queue(100)
midi_out_bus = Queue(200)
ticker_bus = Queue(100)
clock_bus = Queue(100)
buttons_bus = Queue()
LEDs_bus = Queue()

def clear_queue(q):
    while not q.empty():
        q.get()
    return
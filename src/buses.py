from queue import Queue
from pykka import ActorRegistry
from constants import debug

midi_in_bus = Queue(100)
midi_out_bus = Queue(200)
ticker_bus = Queue(100)
clock_bus = Queue(100)

OLED_bus = Queue(100)
encoder_in_bus = Queue(100)
encoder_out_bus = Queue(100)
button_grid_bus = Queue(100)
LED_grid_bus = Queue(100)

def clear_queue(q):
    while not q.empty():
        q.get()
    return

class Bus_Registry(object):
    def __init__(self):
        self.registry = {}
    def get(self, name):
        debug("get")
        debug(name)
        debug(self.registry.get(name))
        return self.registry.get(name)
    def add(self, name, bus):
        debug("add")
        debug(name)
        debug(bus)
        self.registry[name] = bus

bus_registry = Bus_Registry()
bus_registry.add('midi_in_bus', midi_in_bus)
bus_registry.add('midi_out_bus', midi_out_bus)
bus_registry.add('ticker_bus', ticker_bus)
bus_registry.add('clock_bus', clock_bus)
bus_registry.add('OLED_bus', OLED_bus)
# bus_registry.add('encoder_button_bus', encoder_button_bus)
# bus_registry.add('encoder_led_bus', encoder_led_bus)
bus_registry.add('button_grid_bus', button_grid_bus)
bus_registry.add('LED_grid_bus', LED_grid_bus)

actor_registry = ActorRegistry

def proxy_registry(name):
    return actor_registry.get_by_class_name('OLED_Screens')[0].proxy()
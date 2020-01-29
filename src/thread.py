from threading import Thread
from queue import Queue
from time import sleep
from constants import debug

class Actor(Thread):
    """A Python Actor"""
    def __init__(self, name, bus_directory):
        Thread.__init__(self, name=name)
        self.daemon = True
        self.name = name
        self.bus_directory = bus_directory
        self.inbox = Queue()
        self.bus_directory.add(self)

    # def start(self):
    #     super(self).start()
    #     return self

    def run(self):
        debug(f"{self.name} started")
        while True:
            sleep(1)
            debug(f"{self.name} default job running")
        return

    def send(self, recipient, msg):
        rec_box = self.bus_directory.mailbox(recipient)
        print(rec_box.qsize())
        rec_box.put(msg)
        return
    
    def get(self):
        return

class Test_Proc(Actor):
    def __init__(self, name, bus_directory, buddy):
        super().__init__(name, bus_directory)
        self.buddy = buddy
    def run(self):
        debug(f"{self.name} started")
        while True:
            # sleep(0.01)
            msg = self.inbox.get()
            debug(f"{self.name} received '{msg}'")
            if len(msg) < 2:
                debug(f"{self.name} stopping")
                break
            debug('..')
            self.send(self.buddy, msg[:-1])
            return



class Bus_Directory(object):
    """Directory to find message bus by actor name"""
    def __init__(self):
        self.directory = {}
    
    def add(self, actor):
        """Register an actor in the directory"""
        self.directory[actor.name] = actor
        return

    def get(self, actor_name):
        """Get handle to whole actor - for important things like killing it"""
        return self.directory.get(actor_name)

    def mailbox(self, actor_name):
        """Look up the inbox for a given actor"""
        return self.directory.get(actor_name).inbox

directory = Bus_Directory()
actor1 = Test_Proc('actor1', directory, 'actor2')
actor2 = Test_Proc('actor2', directory, 'actor1')
directory.mailbox('actor1').put('abcdefghijklmnopqrstuvqxyz')
sleep(1)
actor1.start()
actor2.start()
sleep(5)
directory.get('actor1')._stop()
directory.get('actor2')._stop()
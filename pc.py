import pycos, random
from sequencer import Sequencer
from time import sleep


def seq_proc(seq, task=None):
    task.set_daemon()
    for i in range(40):
        yield seq.step_beat()
        sleep(0.05)

def server_proc(task=None):
    task.set_daemon()
    while True:
        msg = yield task.receive()
        print('received %s' % (msg))

msg_id = 0

def client_proc(server, n, task=None):
    global msg_id
    for x in range(3):
        yield task.suspend(random.uniform(0.5, 3))
        msg_id += 1
        server.send('%d: %d / %d' % (msg_id, n, x))

seq = Sequencer(bars=4)
server = pycos.Task(server_proc)
seqproc = pycos.Task(seq_proc, seq)
for i in range(10):
    pycos.Task(client_proc, server, i)

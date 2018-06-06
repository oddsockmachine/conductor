from __future__ import print_function
import sys
import mido
from time import sleep, time


beatclockcount = 0
if len(sys.argv) > 1:
    portname = sys.argv[1]
else:
    portname = "Flynn"  # Use default port

try:
    with mido.open_input('Flynn_In', autoreset=True, virtual=True) as port:
        print('Using {}'.format(port))
        print('Waiting for messages...')
        start_time = time()
        print(start_time)
        while True:
            sleep(1)
            for message in port.iter_pending():
                # if message.type == "clock":
                beatclockcount += 1
                print('.', end='')
                print(message)
                sys.stdout.flush()
            print(beatclockcount)
            beatclockcount = 0

except KeyboardInterrupt:
    pass

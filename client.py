from time import sleep
import socket

if __name__ == "__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("localhost", 9009))
    for i in range(5):
        data = b"some data"
        sock.sendall(data)
        sleep(1)
        result = sock.recv(1024)
        print(result)
    sock.close()



# import asyncio
# import random
#
# q = asyncio.Queue()
#
#
# async def producer(num):
#     while True:
#         await q.put(num + random.random())
#         await asyncio.sleep(random.random())
#
# async def consumer(num):
#     while True:
#         value = await q.get()
#         print('Consumed', num, value)
#
# loop = asyncio.get_event_loop()
#
# for i in range(6):
#     loop.create_task(producer(i))
#
# for i in range(3):
#     loop.create_task(consumer(i))
#
# loop.run_forever()

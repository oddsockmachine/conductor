from time import sleep
import logging
import multiprocessing
import socket
# from asyncio import Queue
from queue import Queue

# def handle(connection, address):
#     import logging
#     logging.basicConfig(level=logging.DEBUG)
#     logger = logging.getLogger("process-%r" % (address,))
#     try:
#         logger.debug("Connected %r at %r", connection, address)
#         while True:
#             data = connection.recv(1024)
#             if data == "":
#                 logger.debug("Socket closed remotely")
#                 break
#             logger.debug("Received data %r", data)
#             connection.sendall(data + " returned")
#             logger.debug("Sent data")
#     except:
#         logger.exception("Problem handling request")
#     finally:
#         logger.debug("Closing socket")
#         connection.close()

class Server(object):

    def __init__(self, hostname, port):
        self.logger = logging.getLogger("server")
        self.hostname = hostname
        self.port = port
        self.foo = Queue()
        # self.foo.put("FFFFFFF")
        # print(self.foo.get())
        # exit()

    def handle_msgs(self, conn, address):
        logging.basicConfig(level=logging.DEBUG)
        # logger = logging.getLogger("process-%r" % (address,))
        try:
            self.logger.debug("Connected %r at %r", conn, address)
            while True:
                data = conn.recv(1024)
                self.setfoo(data)
                if data == "":
                    self.logger.debug("Socket closed remotely")
                    break
                self.logger.debug("Received data %r", data)
                conn.sendall(data + b" returned")
                # self.logger.debug("Sent data")
                # print(self.foo.qsize())
        except:
            self.logger.exception("Problem handling request")
        finally:
            self.logger.debug("Closing socket")
            conn.close()

    def run_seq(self):
        while True:
            print(".")
            try:
                item = self.foo.get()
                print(item)
            except:
                print("?")
                pass
            sleep(0.5)

    # def getfoo(self):
    #     print("getting")
    #     item = await self.foo.get()
    #     return item
        # print(item)
        # return item

    def setfoo(self, f):
        self.foo.put(f)

    def start(self):
        self.logger.debug("listening")
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.hostname, self.port))
        self.socket.listen(1)

        while True:
            conn, address = self.socket.accept()
            self.logger.debug("Got connection")
            msg_process = multiprocessing.Process(target=self.handle_msgs, args=(conn, address))
            seq_process = multiprocessing.Process(target=self.run_seq)
            msg_process.daemon = True
            seq_process.daemon = True
            msg_process.start()
            seq_process.start()
            self.logger.debug("Started process %r", msg_process)
            self.logger.debug("Started process %r", seq_process)


if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.DEBUG)
    server = Server("0.0.0.0", 9009)
    try:
        logging.info("Starting server")
        server.start()
    except:
        logging.exception("Unexpected exception")
    finally:
        logging.info("Shutting down")
        for process in multiprocessing.active_children():
            logging.info("Shutting down process %r", process)
            process.terminate()
            process.join()
    logging.info("All done")

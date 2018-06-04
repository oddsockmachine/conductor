from time import sleep
import socket

if __name__ == "__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("localhost", 9000))
    for i in range(10):
        data = "some data" + str(i)
        sock.sendall(data)
        sleep(0.5)
        result = sock.recv(1024)
        print result
    sock.close()

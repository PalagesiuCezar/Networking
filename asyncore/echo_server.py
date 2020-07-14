import asyncore
import socket

BUFSIZE = 4096

class EchoHandler(asyncore.dispatcher_with_send):
    def handle_read(self):
        read = self.recv(BUFSIZE)
        print(read)
        if read:
            self.send(read)

class EchoServer(asyncore.dispatcher):
    def __init__(self,server_host,server_port,backlog = 5):
        asyncore.dispatcher.__init__(self)

        self.create_socket(socket.AF_INET,socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((server_host,server_port))
        self.listen(backlog)
        print(1)

    def handle_accept(self):
        socket_coonection , socket_address = self.accept()
        print("incoming client {}:{}".format(socket_address[0],socket_address[1]))
        handler = EchoHandler(socket_coonection)

if __name__=="__main__":
    server = EchoServer('192.168.1.3',8080)
    asyncore.loop()

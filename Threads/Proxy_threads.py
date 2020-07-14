import config
import socket
import threading
import pickle
import time

class Treads(threading.Thread):

    def __init__(self,socket_server1,socket_server2):
        super(Treads,self).__init__()
        self.socket_server1 = socket_server1
        self.socket_server2 = socket_server2

    def run(self):
        self.MAX_RECV = 1024
        self.client_socket, self.client_addr = self.socket_server1.accept()
        print("client just connected {}:{}".format(self.client_addr[0], self.client_addr[1]))

        try:
            self.data_string = pickle.dumps(self.recvall(self.client_socket, self.MAX_RECV))
            if not self.data:
                print("client jus disconected")
                self.client_socket.close()
                self.socket_server2.close()
            print("sending data to server...")
            self.socket_server2.send(self.data_string)
            print("data has been send...")
        except socket.error as errr:
            print(errr)

        try:
            self.data2 = self.socket_server2.recv(self.MAX_RECV)
            print("recieved data back from server.")

            if not self.data2:
                print("server stopped working")
                self.client_socket.close()
                self.socket_server2.close()
            print("sending data to client...")
            self.client_socket.send(self.data2)
            print("data has been send..")
        except socket.error as serr:
            print(serr)

    def recvall(self, client_socket, MAX_RECV_BUFF):
        self.client_socket = client_socket

        self.MAX_RECV_BUFF = MAX_RECV_BUFF

        self.total_data = []
        self.data = ""

        self.recv_size = 1

        while self.recv_size:
            self.data = client_socket.recv(self.MAX_RECV_BUFF)
            if not len(self.data):
                break
            else:
                self.total_data.append(self.data)
            self.recv_size = len(self.data)
            self.data = ""
        return self.total_data


class Proxy_server():
    def __init__(self,server_address=(('127.0.0.1',8080)),server_address2=(('127.0.0.1',8081))):
        self.server_address=server_address
        self.server_address2=server_address2

        self.socket_server1=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

        try:
            self.socket_server1.bind(server_address)
            print("server successfully binded")
        except socket.error as err:
            print("cant bind cuz {}".format(err))

        self.socket_server1.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        if hasattr(socket, "SO_REUSEPORT"):
            self.socket_server1.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)

        self.socket_server1.listen(5)

        self.socket_server2=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        try:
            self.socket_server2.connect(server_address2)
        except socket.error as err:
            print(str(err))

        self.start_server()

    def start_server(self):
        try:
            while True:
                self.handle(self.socket_server1,self.socket_server2)
                time.sleep(1)
        except KeyboardInterrupt:
            self.shutdown()

    def shutdown(self):
        print("server is closing...")
        self.socket_server1.close()

    def handle(self,socket_server1,socket_server2):
        self.socket_server1=socket_server1
        self.socket_server2=socket_server2

        self.client_handler=Treads(socket_server1,socket_server2)

if __name__=="__main__":
    muie=Proxy_server()
    muie.start_server()
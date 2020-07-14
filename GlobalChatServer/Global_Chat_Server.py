import socket
import select
import sys
import logging
from configparser import ConfigParser
from queue import Queue

class Server(object):
    def __init__(self,setBlocking=False,port=8080,resueAddr=True,server_addr=None,backLog=10):
        self.port=port
        self.socket_server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

        if server_addr is None:
            self.server_address=("127.0.0.1",port)
        else:
            self.server_address=socket.gethostbyname(socket.gethostname())

        try:
            self.socket_server.bind(self.server_address)
            print("server successfully binded at {}:{}".format(self.server_address[0],self.server_address[1]))
        except socket.error:
            print("couldn't bind this server...")

        if setBlocking:
            self.socket_server.setblocking(0)

        if resueAddr:
            self.socket_server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)

        self.socket_server.listen(10)

        self.inputs=[self.socket_server]
        self.outputs=[]

    def start_server(self):

        self.server_status=True

        while self.server_status:

            readable,writeable,exceptional=select.select(self.inputs,self.outputs,self.inputs)

            for sock in readable:
                if sock==self.socket_server:

                    socket_client,socket_addr=self.socket_server.accept()
                    self.inputs.append(socket_client)
                    print("client just connected {}:{}".format(socket_client[0],socket_client[1]))
                    self.recvmessage(socket_client)

            for sock in writeable:
                if sock==self.socket_server:
                    socket_client.send(self.outputs[self.data])
                    self.outputs.remove(self.data)

            for sock in exceptional:
                if sock==self.socket_server:
                    self.dissconect_client()

    def recvmessage(self,socket_client):
        MAX_RECV_BUFFER=1024
        try:
            self.data=socket_client.recv(MAX_RECV_BUFFER)
        except socket.error as err:
            print(str(err))
        self.outputs.append(self.data)

    def dissconect_client(self):
        if self.data in self.outputs:
           #self.outputs.remove(self.data)
            del self.outputs[self.data]
        if socket_client in self.inputs:
           #self.inputs.remove(self.socket_client)
            del self.inputs[socket_client]

    def shut_down(self):
        self.socket_server.close()


if __name__=="__main__":
    chat=Server().start_server()

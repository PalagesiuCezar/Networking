import threading
import socket
import config
import subprocess

class Treads(threading.Thread):
    
    def __init__(self,client_scoket,client_addr):
        super(Treads, self).__init__()

        self.client_socket=client_scoket
        self.client_addr=client_addr

    def run(self):
        MAX_RECV = 1024
        self.allowed_commands = ['ls', 'cd', 'ls -l']

        self.recv_size = 1
        while self.recv_size:

            self.data = self.client_socket.recv(MAX_RECV)
            self.command = self.data.decode('utf-8')
            if not self.data:
                print("clinet just disconected")
                break

            self.recv_size = len(self.data)
            if self.command in self.allowed_commands:
                self.response = self.run_command(self.command)
                self.client_socket.send(self.response.encode('utf-8'))

            self.data = ""

    def run_command(self, command):
        try:
            output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
            return str(output)
        except OSError as oserr:
            return print("there is no command mata i curva {}:{}".format(output, oserr))


class Telnet_server(object):
    def __init__(self,setBlocking=False,port=8080,server_adrress='127.0.0.1'):

        self.socket_server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

        if server_adrress:
            try:
                self.socket_server.bind((server_adrress,port))
                print("server successfully binded")
            except socket.error as serr:
                print("erroare boy {}".format(str(serr)))
        else:
            print("Nu exista nici-o adresa")

        self.socket_server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        if hasattr(socket,"SO_REUSEPORT"):
            self.socket_server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEPORT,1)

        if setBlocking:
            self.socket_server.setblocking(0)

        try:
            self.socket_server.listen(1)
        except socket.error as err:
            print(str(err))

        self.start_server()

    def start_server(self):

        try:
            while True:
                self.handle()

        except KeyboardInterrupt:
            self.shutdown()

    def shutdown(self):
        print("server is closing...(trei puncte mata i curva mati)")
        self.socket_server.close()

    def handle(self):

        self.client_socket, self.client_addr = self.socket_server.accept()

        print("client just connected {}:{}".format(self.client_addr[0], self.client_addr[1]))

        self.client_handler=Treads(self.client_socket,self.client_addr)
if __name__=="__main__":
    muie=Telnet_server()
    muie.start_server()
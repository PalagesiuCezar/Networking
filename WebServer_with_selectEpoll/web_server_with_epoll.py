import socket
import select
import argparse
import sys

SERVER_HOST = ' localhost'
EOL1 = b'\n\n'
EOL2 = b'\n\r\n'
SERVER_RESPONSE = b"""HTTP/1.0 200 OK\r\nDate: Mon, 1 Jan 1996 01:01:01 GMT\r\nContent-Type: text/plain\r\nContent-Length: 13\r\n\r\nHELOOWWW FROM THIS SERVERR"""

class EpollServer(object):
    def __init__(self,host = SERVER_HOST ,port = 0):

        reuse_address=True
        set_blocking = False

        self.socket_server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

        if reuse_address:
            self.socket_server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            if hasattr(socket,"SO_REUSEPORT"):
                self.socket_server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEPORT,1)
        if set_blocking:
            self.socket_server.setblocking(1)

        try:
            self.socket_server.bind((host,port))
        except socket.error as err:
            print("could not bind the server address {}" .format(err))
            sys.exit(1)

        self.socket_server.listen(5)

        self.socket_server.setsockopt(socket.IPPROTO_TCP,socket.TCP_NODELAY,1)

        print("Start epoll server...")

        self.epoll = select.epoll()
        self.epoll = register(self.socket_server.fileno(),select.EPOLLIN)

        server_status = True

        def start_server(self):
            try:
                connections = {}; requests = {}; responses = {};
                while server_status:
                    events = self.epoll.poll(1)

                    for fileno,event in events:
                        if fileno == self.socket_server.fileno():
                            client_socket,client_addr = self.socket_server.accept()
                            client_socket.setblockin(0)

                            self.epoll.register(client_socket.fileno(),select.EPOLLIN)

                            connections[client_socket.fileno()] = client_socket
                            requests[client_socket.fileno()] = b''
                            responses[client_socket.fileno()] = SERVER_RESPONSE

                        elif event and select.EPOLLIN:
                            requests[fileno] += connections[fileno].recv(1024)

                            if EOL1 in requests[fileno] or EOL2 in requests[fileno]:
                                self.epoll.modify(fileno,select.EPOLLOUT)
                                print('-'*40 + '\n' + requests[fileno].decode()[:-2])
                            elif event and select.EPOLLOUT:
                                byteswritten = connections[fileno].send(responses[fileno])
                                responses[fileno] = responses[fileno][byteswritten:]

                                if len(responses[fileno]) == 0:
                                    self.epoll.modify(fileno, 0)
                                    connections[fileno].shutdown(socket.SHUT_RDWR)
                                elif event and select.EPOLLUP:
                                    self.epoll.unregister(fileno)
                                    connections[fileno].close()
                                    del connections[fileno]
            finally:
                self.epoll.unregister(self.socket_server.fileno())
                self.epoll.close()
                self.socket_server.close()

if __name__=="__main__":
    arg_parse = argparse.ArgumentParser(description="Socket Server Example")
    arg_parse.add_argument('--port' , action = "store" , dest = "port" , type = int , required = False)
    given_args = arg_parse.parse_args()
    port = given_args.port
    server = EpollServer(host = SERVER_HOST, port = port)
    server.start_server()

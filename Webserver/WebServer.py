import socket


class Webserver(object):
    def __init__(self, server_address=None, setBlocking=False, reuse_addr=True, port=8089):

        self.socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        if server_address is not None:
            self.server_address = (server_address, port)
        else:
            self.server_address = ('', port)

        try:
            self.socket_server.bind((self.server_address))
        except IOError as err:
            print(str(err))

        print("server succesfully binded at {}:{}".format(self.server_address[0],self.server_address[1]))

        if reuse_addr:
            self.socket_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            if hasattr(socket,"SO_REUSEPORT"):
                self.socket_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)

        if setBlocking:
            self.socket_server.setBlocking(1)

        self.socket_server.listen(10)

    def start_server(self):

        server_status = True

        while server_status:
            try:
                self.handle_server()
            except KeyboardInterrupt as kerr:
                print(kerr)
                self.shutdown_server()

    def handle_server(self):

        client_socket, client_addr = self.socket_server.accept()

        print("client connected {}:{}".format(client_socket[0], client_socket[1]))

        request = client_socket.recv(1024).decode("utf-8")
        print(request)

        http_request = """\
HTTP/1.1 200 OK

Hello world!
"""

        client_socket.sendall(http_request).encode("utf-8")
        client_socket.close()

    def shutdown_server(self):
        self.socket_server.close()
        print("server is closing...")


if __name__ == "__main__":
    wb = Webserver
    wb.start_server()

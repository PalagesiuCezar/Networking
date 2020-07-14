import os
import socket
import threading

try:
    import SocketServer
except ModuleNotFoundError:
    import socketserver

SERVER_HOST = 'localhost'
SERVER_PORT = 0 #tells the kernel to pick up a port dinamically
BUF_SIZE = 1024

def client(ip,port,message):
    client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client_socket.connect((ip,port))

    try:
        client_socket.sendall(message.encode("utf-8"))
        response = client_socket.recv(BUF_SIZE).decode("utf-8")

        print("Client received : {}" .format(response))
    finally:
        client_socket.close()

class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):
    def handle(self):

        data = self.request.recv(1024).decode("utf-8")

        current_thread = threading.current_thread()
        response = "{} : {} ".format(current_thread.name,data)

        self.request.sendall(response.encode("utf-8"))

class ThreadedTCPServer(SocketServer.ThreadingMixIn,SocketServer.TCPServer):
    pass

if __name__=="__main__":
    server = ThreadedTCPServer((SERVER_HOST,SERVER_PORT),ThreadedTCPRequestHandler)

    ip,port = server.server_address
    server_thread = threading.Thread(target = server.serve_forever)
    server_thread.daemon = True
    server_thread.start()

    print("Server loop runing on thread : {}".format(server_thread.name))

    client(ip,port,"heyaa bitch")
    client(ip,port, "gotti man")
    client(ip,port, " dupa blocuri ")

    server.shutdown()

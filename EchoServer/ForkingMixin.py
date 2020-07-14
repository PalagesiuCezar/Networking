import os
import socket
import threading
try:
    import SocketServer #run in python2
except ModuleNotFoundError:
    import socketserver #python3
except NameError:
    import socketserver # --/--

SERVER_HOST = 'localhost'
SERVER_PORT = 0 #tells kernel to pick up a port dinamically
BUF_SIZE = 1024
ECHO_MSG = 'HELLO ECHO SERVER'

class ForkedClient():
    def __init__(self,ip,port):
        self.socket_client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.socket_client.connect((ip,port))

    def run(self):

        current_process_id = os.getpid()
        print("PID {} Sending echo messaje to the server : {} " .format(current_process_id,ECHO_MSG))

        sent_data_lenght = self.socket_client.send(ECHO_MSG.encode("utf-8"))
        print("Sent : {} characters , so far..." .format(sent_data_lenght))

        response = self.socket_client.recv(BUF_SIZE)
        print("PID {} recieved : {} " .format(current_process_id,response[5:]))

    def shutdown(self):
        self.socket_client.close()

class ForkingServerRequestHandler(SocketServer.BaseRequestHandler):
    def handle(self):

        data = self.request.recv(BUF_SIZE)
        current_process_id = os.getpid()
        response = '{} : {}' .format(current_process_id,data)

        print("Server sending response [current_process_id: data] = [{}]".format(response))

        self.request.send(response)
        return

class ForkingServer(SocketServer.ForkingMixIn,
                    SocketServer.TCPServer,
                    ):
    pass

def main():
    server = ForkingServer((SERVER_HOST,SERVER_PORT),ForkingServerRequestHandler)

    ip,port = server.server_address

    server_thread = threading.Thread(target = server.serve_forever)
    server_thread.setDaemon(True)
    server_thread.start()

    print("Server loop runing PID : {}".format(os.getpid()))

    client1 = ForkedClient(ip,port)
    client1.run()

    client2 = ForkedClient(ip,port)
    client2.run()

    client3 = ForkedClient(ip,port)
    client3.run()

    server.shutdown()
    client1.shutdown()
    client2.shutdown()
    client3.shutdown()
    server.socket.close()

if __name__=="__main__":
    main()

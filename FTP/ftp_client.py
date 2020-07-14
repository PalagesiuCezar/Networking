import socket
import os
import struct

class FTPClient(object):

    BASE_FOLDER = os.path.dirname(os.path.abspath(__file__))
    FILENAME='mata1027'
    def __init__(self, server_address,reuseAddr=True):
        self.server_address = server_address
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        if reuseAddr:
            self.client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.client_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEPORT,1)
    def start_client(self):
        try:
            self.client_socket.connect(self.server_address)
            print("[*] Just connected at {}:{}".format(self.server_address[0], self.server_address[1]))
            self.download_file(FTPClient.FILENAME)
        except OSError:
            print("[*] Couldn`t connect.")

    def download_file(self, filename):
        with open(filename,'w') as f:
            print("file opened...")
            self.rec_data=''
            self.size=1
            while self.size:
                self.size=""
                print("reciving data...")
                self.data = self.client_socket.recv(1024)
                self.data = self.data.decode('utf-8')
                self.size=self.data
                self.rec_data+=self.data
            f.write(self.rec_data)
        self.client_socket.close()

if __name__ == "__main__":
    ftp = FTPClient(("127.0.0.1", 8089))
    ftp.start_client()
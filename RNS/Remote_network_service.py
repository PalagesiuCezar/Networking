import socket
import errno
from time import time as now

DEFAULT_TIMEOUT = 120

class NetworkServiceChecker(object):
    def __init__(self, host , port , timeout = DEFAULT_TIMEOUT):

        self.host = host
        self.port = port
        self.timeout = timeout

        self.socket_server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    def end_net(self):

        self.socket_server.close()

    def check(self):

        if self.timeout:
            end_time = now() + self.timeout
        else:
            print(1)

        while True:
            try:
                if self.timeout:
                    next_timeout = end_time -now()

                    if next_timeout < 0:
                        return False
                    else:
                        print("setting socket for the next timeout {}" .format(round(next_timeout)))

                        self.socket_server.settimeout(next_timeout)
                self.socket_server.connect((self.host,self.port))

            except socket.timeout as e:
                if self.timeout:
                    return False

            except socket.error as e:
                print("exception {}" .format(e))

            else:
                self.end_net()
                return True

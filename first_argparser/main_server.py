import sys
import socket
import argparse

def Server():

    args_parser = argparse.ArgumentParser(description='Socket Error Examples')

    args_parser.add_argument('--host',action="store",dest="host",required=False)
    args_parser.add_argument('--port',action="store",dest="port",type=int,required=False)
    args_parser.add_argument('--file',action="store",dest="file",required=False)

    args=args_parser.parse_args()
    host = args.host
    port = args.port
    filename = args.file

    try:
        socket_server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    except socket.error as e:
        print("error creatin the socket {} ".format(e))
        sys.exit(1)

    try:
        socket_server.connect((host,port))
    except socket.gaierror as e:
        print(" can't connect to server : {}".format(e))
        sys.exit(1)
    except socket.error as e:
        print("connection error {} " .format(e))
        sys.exit(1)

    try:
        socket_server.sendall("GET %s HTTP/1.1\r\n\r\n" % filename).encode("utf-8")
    except socket.error as e:
        print("error sending data {}".format(e))
        sys.exit(1)

    while(True):
        try:
            recv_buffer = socket_server.recv(2048)
        except socket.error as e:
            print("error reciving data {} ".format(e))
            sys.exit(1)
        if not len(recv_buffer):
            break
        sys.stdout.write(recv_buffer)

if __name__=="__main__":
    Server()

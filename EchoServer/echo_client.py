import socket
import sys
import argparse

def echo_client(host,port):
    socket_server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    server_address = (host,port)

    socket_server.connect(server_address)

    try:
        message = "this message will be echoed"
        print("sending {}" .format(message))
        socket_server.sendall(message.encode("utf-8"))

        amount_received = 0
        amount_excepted = len(message)

        while amount_received < amount_excepted:
            data = socket_server.recv(16).decode("utf-8")
            amount_received += len(data)
            print("recevied : {}".format(data))

    except socket.errno as e:
        print("socket error : {}" .format(str(e)))
        sys.exit(1)

    except Exception as e:
        print("Other exceptions : {}" .format(str(e)))
        sys.exit(1)

    finally:
        print("Closing connection to the server...")
        socket_server.close()
        sys.exit(1)

if __name__=="__main__":
    args_parse = argparse.ArgumentParser(description="Socket Server Example")
    args_parse.add_argument('--host' , action = "store" , dest = "host" , required = False)
    args_parse.add_argument('--port' , action = "store" , dest = "port" , type = int , required = False)
    given_args = args_parse.parse_args()
    host = given_args.host
    port = given_args.port

    echo_client(host,port)

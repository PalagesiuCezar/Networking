import socket
import sys
import argparse

data_payload = 2048
backlog = 5

def echo_server(host,port):
    socket_server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    socket_server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    if hasattr(socket,"SO_REUSEPORT"):
        socket_server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEPORT,1)

    server_address = (host,port)

    socket_server.bind(server_address)
    socket_server.listen(backlog)
    print("server is listening on {} : {} ".format(server_address[0],server_address[1]))

    while(True):
        print("waiting to recv a massage : ")

        client_socket,address_socket = socket_server.accept()
        data = client_socket.recv(data_payload).decode("utf-8")

        if data:
            print("Data:  {}".format(data))
            client_socket.send(data.encode("utf-8"))
            print("sent {} bytes back to {}".format(data,address_socket[0]))
        client_socket.close()

if __name__=="__main__":
    arg_parse = argparse.ArgumentParser(description="Socket Server Example")
    arg_parse.add_argument('--host' , action = "store" , dest = "host" , required = False)
    arg_parse.add_argument('--port' , action = "store" , dest = "port" , type = int , required = False)
    given_args = arg_parse.parse_args()
    host = given_args.host
    port = given_args.port
    
    echo_server(host,port)

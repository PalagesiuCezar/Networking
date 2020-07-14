import socket

def init_server(server_address):
    socket_server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    try:
        print("[*] Client is trying to connect at {}:{}".format(server_address[0], server_address[1]))
        socket_server.connect(server_address)
    except socket.error as serr:
        print("unable to connect {}".format(serr))
        socket_server.close()

    print("[*] Client has successfuly connected at {}:{}".format(server_address[0],server_address[1]))

    recv_all(socket_server)

def recv_all(socket_server):
    MAX_RECV=1024
    command = input("type: ")
    try:

        socket_server.send(command.encode("utf-8"))

        data=socket_server.recv(MAX_RECV).decode('utf-8')
        print("{} \n".format(data))

        command=input("$~")
        data=""

    except KeyboardInterrupt as kerr:
        print("[*] You left this server")

if __name__=="__main__":
    init_server(("10.10.2.223",8080))
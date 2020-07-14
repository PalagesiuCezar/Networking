import socket

def init_server(server_address):
    socket_server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    try:
        socket_server.connect(server_address)
    except socket.error as serr:
        print("unable to connect {}".format(serr))
        socket_server.close()

    print("just connected at {}:{}".format(server_address[0],server_address[1]))

    recv_all(socket_server)

def recv_all(socket_server):
    MAX_RECV=1024

    allowed_commands=['ls','cd','ls -l']

    try:
        command=input("$~")
        while command!="exit":
            if command in allowed_commands:

                socket_server.send(command.encode('utf-8'))

                data=socket_server.recv(MAX_RECV)
                print("{} \n".format(data.decode('utf-8')))

                command=input("$~")
                data=""
            elif command=="exit":
                print("You left this server")
            else:
                print("Command {} is not allowed".format(command))
                command=input("$~")
    except KeyboardInterrupt as kerr:
        print("You left this server")

if __name__=="__main__":
    init_server(("127.0.0.1",8089))

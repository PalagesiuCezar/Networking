import socket
import subprocess
import confirguri

def init_server(server_address):
    socket_server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    try:
        print("[*] Server is trying to bind to address {}:{}".format(server_address[0], server_address[1]))
        socket_server.bind(server_address)
        print("[*] Server has successfuly binded.")
    except socket.error as serr:
        print(str(serr))

    socket_server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    if hasattr(socket,"SO_REUSEPORT"):
        socket_server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEPORT,1)

    socket_server.listen(5)

    print("[*] Server listen at {}:{}".format(server_address[0],server_address[1]))

    try:
        while True:
            client_socket,client_addr=socket_server.accept()
            print("[*] Client has connected {}:{}".format(client_addr[0],client_addr[1]))
            handle(client_socket)
    except KeyboardInterrupt as kerr:
        print("[*] Server is closing...")
        socket_server.close()

def handle(client_socket):
    MAX_RECV=1024

    recv_size=1
    while recv_size:
        data=client_socket.recv(MAX_RECV).decode('utf-8')

        if not data:
            print("[*] Client just disconected")
            break

        recv_size=len(data)
        client_socket.send(data.encode("utf-8"))
        data=""

if __name__=="__main__":
    init_server(("10.10.2.223",8080))
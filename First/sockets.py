import socket
import subprocess

def init_server(server_address):
    socket_server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    try:
        socket_server.bind(server_address)
    except socket.error as serr:
        print(str(serr))

    socket_server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    if hasattr(socket,"SO_REUSEPORT"):
        socket_server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEPORT,1)

    socket_server.listen(5)

    print("server listen at {}:{}".format(server_address[0],server_address[1]))

    try:
        while True:
            client_socket,client_addr=socket_server.accept()
            print("client has connected {}:{}".format(client_addr[0],client_addr[1]))

            handle(client_socket)
    except KeyboardInterrupt as kerr:
        print("server is closing...")
        client_socket.close()
        socket_server.close()

def handle(client_socket):
    MAX_RECV=1024

    allowed_commands=['ls','cd','ls -l']

    recv_size=1
    while recv_size:
        data=client_socket.recv(MAX_RECV)
        command=data.decode('utf-8')

        if not data:
            print("client just disconected")
            break
        recv_size=len(data)

        if command in allowed_commands:
            response=run_command(command)
            client_socket.send(response.encode("utf-8"))
        data=""

def run_command(command):
    try:
        output=subprocess.check_output(command,stderr=subprocess.STDOUT,shell=True)
        return str(output)
    except OSError as oserr:
        return output

if __name__=="__main__":
    init_server(("127.0.0.1",8089))
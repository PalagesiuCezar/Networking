import socket
import threading

port_list_rele=[]
port_list_bune=[]

def port_scanner(server_address,port):

    socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:

        socket_server.connect((server_address,port))

    except socket.error as err:

        port_list_rele.append(port)
    else:
        port_list_bune.append(port)
        socket_server.close()
if __name__=="__main__":
    server_address='127.0.0.1'
    port=1000

    for i in range(0,port):

        thread = threading.Thread(target=port_scanner, args=(server_address,i))
        thread.start()

    print(port_list_rele)
    print(port_list_bune)
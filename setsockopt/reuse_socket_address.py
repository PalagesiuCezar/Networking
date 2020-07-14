import socket
import sys

def resuse_socket_addr():
    socket_server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    old_state = socket_server.getsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR)
    print("the old sock is {} " .format(old_state))

    socket_server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    new_state = socket_server.getsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR)
    print("the new sock is {}" .format(new_state))

    port = 8080

    the_socket_servet = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    the_socket_servet.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    the_socket_servet.bind(('',port))
    the_socket_servet.listen(1)
    print("listening on port {} " .format(port))

    while(True):
        try:
            client_sock,client_addr = the_socket_servet.accept()
            print("connected by {}:{}" .format(client_addr[0],client_addr[1]))
        except KeyboardInterrupt:
            print("is closing...")
            break
            sys.exit(1)
        except socket.error as msg:
            print("the error is  {} ".format(msg))

if __name__=="__main__":
    resuse_socket_addr()

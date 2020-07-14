import socket

SEND_BUF_SIZE = 4096
RECV_BUF_SIZE = 4096

def modif_bufffer_size():
    socket_server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    buffsize = socket_server.getsockopt(socket.SOL_SOCKET,socket.SO_SNDBUF)
    print("buffer size [Before] : {}" .format(buffsize))

    socket_server.setsockopt(socket.SOL_TCP,socket.TCP_NODELAY,1)
    socket_server.setsockopt(
            socket.SOL_SOCKET,
            socket.SO_SNDBUF,
            SEND_BUF_SIZE
            )
    socket_server.setsockopt(
            socket.SOL_SOCKET,
            socket.SO_RCVBUF,
            RECV_BUF_SIZE
            )
    buffsize = socket_server.getsockopt(socket.SOL_SOCKET,socket.SO_SNDBUF)
    print("buffer size [After] : {}" .format(buffsize))

if __name__=="__main__":
    modif_bufffer_size()

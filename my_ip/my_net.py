import sys
import socket
import fcntl
import struct
import array

SIOCGIFCONF = 0x8912
STUCT_SIZE_32 = 32
STUCT_SIZE_64 = 40
PLATFORM_32_MAX_NUMBER = 2**32
DEFAULT_INTERFACES = 8

def list_interfaces():

    interfaces = []
    max_interfaces = DEFAULT_INTERFACES

    is_64bits = sys.maxsize > PLATFORM_32_MAX_NUMBER
    struct_size = STUCT_SIZE_64 if is_64bits else STUCT_SIZE_32

    socket_server = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    while True:
        bytess = max_interfaces * struct_size
        interface_name = array.array('B','\0' *bytess)
        sock_info = fcntl.ioctl(socket_server.fileno(),
                                SIOCGIFCONF,
                                struct.pack('iL',bytess,interface_name.buffer_info()[0]))

        outbytes = struct.unpack('iL',sock_info)[0]

        if outbytes == bytes:
            max_interfaces *= 2
        else:
            break

        namestr = interface_name.tostring()

        for i in range(0,outbytes,struct_size):
            interfaces.append((namestr[i:i+16].split('\0',1)[0]))

        return interfaces

if __name__=="__main__":
    interfaces = list_interfaces()
    print(interfaces)
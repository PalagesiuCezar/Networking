import socket
import struct
import sys
import time

NTP_SERVER = '0.uk.pool.ntp.org'
TIME1970 = 2208988800L # 1970-01-01 00:00:00

def sntp_client():
    socket_server = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    data = '\x1b' + 47 * '\0'
    socket_server.sendto(data,(NTP_SERVER,123))
    data,address = socket_server.recvfrom(1024)

    if data:
        print("response received from : {} ".format(address))

    tim = struct.unpack('!12I',data)[10]
    tim -= TIME1970
    print("\tTime = {}".format(time.ctime(tim)))

if __name__=="__main__":
    sntp_client()

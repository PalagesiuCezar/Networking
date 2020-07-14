import socket
import struct
import binascii
import os
import packets
import time

def sniffer():
    if os.name == "nt":
        s = socket.socket(socket.AF_INET,socket.SOCK_RAW,socket.IPPROTO_IP)
        s.bind(("YOUR_INTERFACE_IP",0))
        s.setsockopt(socket.IPPROTO_IP,socket.IP_HDRINCL,1)
        s.ioctl(socket.SIO_RCVALL,socket.RCVALL_ON)

    else:
        s=socket.socket(socket.PF_PACKET, socket.SOCK_RAW, socket.ntohs(0x0003))

    server_status = True

    while server_status:

        data=s.recvfrom(65565)
        unpack=packets.unpack()

        print("\n\n----------------------------------ETHERNET HEADER--")
        for i in unpack.eth_header(data[0][0:14]).iteritems():
            a,b=i
            print("{} : {} | ".format(a,b))
        time.sleep(3)
        print("\n------------------------------------------IP HEADER--")
        for i in unpack.ip_header(data[0][14:34]).iteritems():
            a,b=i
            print("{} : {} | ".format(a,b))
        time.sleep(3)
        print("\n------------------------------------------TCP HEADER--")
        for  i in unpack.tcp_header(data[0][34:54]).iteritems():
            a,b=i
            print("{} : {} | ".format(a,b))
        time.sleep(3)
        print("\n------------------------------------------UDP HEADER--")
        for i in unpack.udp_header(data[0][54:62]).iteritems():
            a,b=i
            print("{} : {} | ".format(a,b))
        time.sleep(3)
        print("\n------------------------------------------ICMP HEADER--")
        for i in unpack.icmp_header(data[0][62:66]).iteritems():
            a,b=i
            print("{} : {} | ".format(a,b))
        time.sleep(3)
        print("\n------------------------------------------ARP HEADER--")
        for i in unpack.arp_header(data[0][66:94]).iteritems():
            a,b=i
            print("{} : {} | ".format(a,b))
        time.sleep(3)

if __name__ == "__main__":
    sniffer()
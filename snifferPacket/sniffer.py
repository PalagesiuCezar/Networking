import socket
import struct
import sys

from packets import *

class SnifferPacket:
    def __init__(self,proto = None , protos = False):

        protocols = {
            "ICMP" : socket.IPPROTO_ICMP,
            "TCP" : socket.IPPROTO_TCP,
            "UDP" : socket.IPPROTO_UDP,
        }

        try:
            if protos:
                self.socket_server = socket.socket(socket.AF_INET,socket.SOCK_RAW,socket.ntohs(0x0003))

            else:

                if proto:
                    self.socket_server = socket.socket(socket.AF_INET,socket.SOCK_RAW,protocols[proto])

        except socket.error as e:
            print(str(e))
            sys.exit(0)

    def run_sniffer(self):

        server_status = True

        try:
            while server_status:

                data = self.socket_server.recvfrom(65565)

                packet = data[0]
                addres = data[1]

                self.proccess_packet(packet)

        except KeyboardInterrupt:
            self.socket_server.close()
            sys.exit(0)

    def proccess_packet(self,packet):

        eth_pack = IP(packet[0:20])
        eth_pack.upper_protocol(packet)
        print(eth_pack)

if __name__=="__main__":
    sniffer = SnifferPacket(proto="TCP")
    sniffer.run_sniffer()
import struct
import platform
from socket import (
    inet_aton,
    inet_ntoa
)
from ctypes import *


class Ethernet(Structure):
    _fields_ = [

        ("dest", c_char * 6),
        ("src", c_char * 6),
        ("type", c_ushort),
    ]

    def __new__(cls, socket_buffer=None):
        return cls.from_buffer_copy(socket_buffer)

    def __init__(self, socket_buffer):
        self.dest_mac = self.nmac_to_host(self.dest)
        self.source_mac = self.nmac_to_host(self.src)

    def __str__(self):
        return "Dest: {} Source: {} Eth Type: {}".format(self.dest_mac,
                                                         self.source_mac, str(hex(self.type)))

    def nmac_to_host(self, _nmac):
        return ':'.join(['%02x' % b for b in _nmac])


class TCP(Structure):
    _fields_ = [

        ("src", c_ushort),
        ("dest", c_ushort),
        ("seq", c_uint),
        ("ack", c_uint),
        ("offset", c_ubyte, 4),
        ("res", c_ubyte, 6),
        ("flags", c_ubyte, 6),
        ("wind", c_ushort),
    ]

    def __new__(cls, socket_buffer=None):
        return cls.from_buffer_copy(socket_buffer)

    def __init__(self, socket_buffer):
        pass

    def __repr__(self):
        pass

    def __str__(self):
        urg = self.flags
        ack = self.flags >> 1
        psh = self.flags >> 2
        rst = self.flags >> 3
        syn = self.flags >> 4
        fin = self.flags >> 5

        return """Sorce Port: {}  Destination Port: {} Ack: {} Seq: {} Urg: {} Ack: {} Psh: {} Rst: {} Syn: {} Fin: {} \n""".format(self.src, self.dest, self.ack, self.seq, self.flags, urg,ack, psh, rst, syn, fin)


class UDP(Structure):
    _fields_ = [

        ("src", c_ushort),
        ("dest", c_ushort),
        ("len", c_ushort),
        ("checksum", c_ushort),
    ]

    def __new__(self, socket_buffer=None):
        return self.from_buffer_copy(socket_buffer)

    def __init__(self, socket_buffer):
        pass

    def __repr__(self):
        pass

    def __str__(self):
        return "Source Port: {} Dest Port: {}".format(self.src, self.dest)


class ARP(Structure):
    _fields_ = [

        ("hardtype", c_ushort),
        ("prototype", c_ushort),
        ("hardlen", c_ubyte),
        ("protolen", c_ubyte),
        ("op", c_ushort),
        ("shdwaddr", c_char * 6),
        ("sipaddr", c_uint, 32),
        ("rechwdaddr", c_char * 6),
        ("recipaddr", c_uint, 32),

    ]

    def __new__(self, socke_buffer=None):
        return self.from_buffer_copy(socket_buffer)

    def __init__(self, socket_buffer):
        pass


class ICMP(Structure):
    _fields_ = [

        ("type", c_ubyte),
        ("code", c_ubyte),
        ("checksum", c_ushort)
    ]

    def __new__(cls, socket_buffer=None):
        return cls.from_buffer_copy(socket_buffer)

    def __init__(self, socket_buffer):
        pass

    def __repr__(self):
        pass

    def __str__(self):
        return "Message Type: {} Messasge Code: {}".format(self.type,
                                                           self.code)


class IP(Structure):
    _fields_ = [

        ("ihl", c_ubyte, 4),
        ("version", c_ubyte, 4),
        ("tos", c_ubyte),
        ("len", c_ushort),
        ("id", c_ushort),
        ("offset", c_ushort),
        ("ttl", c_ubyte),
        ("protocol_t", c_ubyte),
        ("sum", c_ushort),
        ("src", c_uint, 32),
        ("dst", c_uint, 32)
    ]

    def __new__(cls, socket_buffer=None):
        return cls.from_buffer_copy(socket_buffer)

    def __init__(self, socket_buffer):

        self.buffer = socket_buffer
        self.protocols = {1: "ICMP",
                          6: "TCP",
                          17: "UDP"}

        self.source_address = inet_ntoa(struct.pack("@I", self.src))
        self.dest_address = inet_ntoa(struct.pack("@I", self.dst))

    # self.upper_proto = self.protocols[self.protocol_t]()

    def __repr__(self):

        pass

    def __str__(self):

        return "Version: {} Source Addr: {} Dest Addr: {}\n{}".format(
            self.version, self.source_address, self.dest_address, str(self.upp_p)
        )

    def upper_protocol(self, buff):

        hdrlen = self.ihl * 4
        up_proto = self.protocols[self.protocol_t]

        if up_proto == "ICMP":

            self.upp_p = ICMP(buff[hdrlen: hdrlen + 4])

        elif up_proto == "TCP":
            self.upp_p = TCP(buff[hdrlen: hdrlen + 20])
            self.upp_p = UDP(buff[hdrlen: hdrlen + 8])
            self.upp_p = Ethernet(buff[hdrlen: hdrlen + 14])

        elif up_proto == "UDP":
            self.upp_p = UDP(buff[hdrlen: hdrlen + 8])
        else:
            pass

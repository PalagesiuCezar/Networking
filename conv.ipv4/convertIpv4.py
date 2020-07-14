import socket
from binascii import hexlify

def convert_ipv4_address():
    for ip_address in ['127.0.0.1','192.168.43.175','192.168.45.173']:
        packed_ip_address = socket.inet_aton(ip_address)
        unpacked_ip_address = socket.inet_ntoa(packed_ip_address)
        print("for {} : packed is {} and unpacked is {} \n".format(ip_address,hexlify(packed_ip_address),unpacked_ip_address))

if __name__=="__main__":
    convert_ipv4_address()

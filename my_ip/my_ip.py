import socket
import fcntl
import struct

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])

ip = get_ip_address('lo')
ip2 = get_ip_address('wlan0')

try:
    ip3 = get_ip_address('eth0')
    print(ip3)
except IOError as err:
    print("You have no eth0 ip...")

print(ip, ip2)
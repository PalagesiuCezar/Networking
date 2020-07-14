
import socket

s = socket.socket()
host = socket.gethostname()
port = 60000

s.connect((host, port))


with open('received_file1', 'wb') as f:
    print('file opened')
    while True:
        print('receiving data...')
        data = s.recv(1024)
        print('data={}'.format(data))
        if not data:
            break
        f.write(data)

f.close()
print('Successfully get the file')
s.close()
print('connection closed')
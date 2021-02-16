import socket


socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = 'localhost'
port = 5555

socket_client.connect((host, port))
socket_client.setblocking(False)
message = 'Test message!' * 10000000
a = socket_client.send(message.encode('utf-8'))
print('Count recieved data - non blocking - mode:' + str(a))
socket_client.send('stop'.encode('utf-8'))
socket_client.close()

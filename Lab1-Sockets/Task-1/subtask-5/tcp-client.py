import socket


ADDRESS = ('127.0.0.1', 5050)
FORMAT = 'utf-8'

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDRESS)

client.setblocking(0)

msg = "Hello Non-Blocking Socket!\n" * 10 * 1024 * 1024
a = client.send(msg.encode(FORMAT))

print('Count recieved data - non blocking - mode:' + str(a))

client.send('stop'.encode(FORMAT))

client.close()

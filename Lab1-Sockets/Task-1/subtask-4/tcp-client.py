import socket


HEADER = 64
ADDRESS = ('127.0.0.1', 5050)
FORMAT = 'utf-8'

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDRESS)


def send(msg):
    message = msg.encode(FORMAT)
    msgLen = len(message)
    sendLen = str(msgLen).encode(FORMAT)
    sendLen += b' '*(HEADER-len(sendLen))
    client.send(sendLen)
    client.send(message)
    print(client.recv(1024).decode(FORMAT))


while True:
    message = input(
        f"Enter message to {ADDRESS[0]}(type \'d\' to disconnect) -> ")
    send(message)
    if message == 'd' or message == 'D':
        break

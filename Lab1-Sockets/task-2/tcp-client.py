import socket
import threading


ADDRESS = ('127.0.0.1', 5050)
FORMAT = 'utf-8'
nickname = input("Enter your nickname:")
print("To left the chat just type 'left'\n")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDRESS)


def receive():
    while True:
        try:
            msg = client.recv(1024).decode(FORMAT)
            if msg == "NICK":
                client.send(nickname.encode(FORMAT))
            else:
                print(msg)
        except:
            print("You're left the chat")
            client.close()
            break


def write():
    while True:
        msg = f'{nickname}: {input("")}'
        client.send(msg.encode(FORMAT))
        if msg[-4:] == "left":
            client.close()
            break


receiveThread = threading.Thread(target=receive)
receiveThread.start()

writeThread = threading.Thread(target=write)
writeThread.start()

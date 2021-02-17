import socket
import threading


ADDRESS = ('127.0.0.1', 5050)
FORMAT = 'utf-8'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDRESS)
server.listen()


clients = []
nicknames = []


def broadcast(msg):
    for client in clients:
        client.send(msg)


def handleClient(client):
    while True:
        try:
            msg = client.recv(1024)
            if msg.decode(FORMAT)[-4:] == "left":
                index = clients.index(client)
                clients.remove(client)
                client.close()
                nickname = nicknames[index]
                broadcast(f'{nickname} left the chat'.encode(FORMAT))
                nicknames.remove(nickname)
                break
            else:
                broadcast(msg)
        except:
            index = client.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f'{nickname} left the chat'.encode(FORMAT))
            nicknames.remove(nickname)
            break


def receive():
    print(f"[LISTENING] Server is listening on {ADDRESS[0]}")
    while True:
        client, addr = server.accept()

        client.send("NICK".encode(FORMAT))
        nickname = client.recv(1024).decode(FORMAT)
        nicknames.append(nickname)
        clients.append(client)

        print(
            f"\n[NEW CONNECTION] {addr} connected with nickname -> {nickname}")
        broadcast(f"{nickname} joined the chat!".encode(FORMAT))
        client.send('Connected to the server!'.encode(FORMAT))

        thread = threading.Thread(target=handleClient, args=(client,))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount()-1}")


print("\n[STARTING] Server is starting...")
receive()

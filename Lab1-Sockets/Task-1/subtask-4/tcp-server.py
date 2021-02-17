import socket
import threading


HEADER = 64
ADDRESS = ('127.0.0.1', 5050)
FORMAT = 'utf-8'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDRESS)


def handleClient(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:
        if conn.recv(HEADER).decode(FORMAT):
            msg = conn.recv(HEADER).decode(FORMAT)
            if msg == 'd' or msg == 'D':
                print(f"[DISCONNECT] {addr} disconnected.")
                connected = False
            else:
                print(f"[{addr}] {msg}")
                conn.send("Message received.".encode(FORMAT))
    conn.close()


def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {ADDRESS[0]}")
    while True:
        client, addr = server.accept()
        thread = threading.Thread(target=handleClient, args=(client, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount()-1}")


print("\n[STARTING] Server is starting...")
start()

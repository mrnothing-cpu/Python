import socket
import threading

host = '127.0.0.1'
port = 55555

#starts the server and listens on 127.0.0.1:55555
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

#Keeps track of all connected client sockets and their usernames (nicknames).
clients = []
nicknames = []

#sends a message to all connected clients
def broadcast(message):
    for client in clients:
        client.send(message)

#
def send_user_list():
    user_list = "USERS:" + ",".join(nicknames)
    for client in clients:
        client.send(user_list.encode('utf-8'))

def handle(client):
    while True:
        try:
            message = client.recv(1024)
            if message:
                broadcast(message)
        except:
            if client in clients:
                index = clients.index(client)
                nickname = nicknames[index]
                clients.remove(client)
                nicknames.remove(nickname)
                client.close()
                broadcast(f'{nickname} left the chat!'.encode('utf-8'))
                send_user_list()
            break

def receive():
    while True:
        client, _ = server.accept()
        client.send('NICK'.encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
        nicknames.append(nickname)
        clients.append(client)
        broadcast(f'{nickname} joined the chat!'.encode('utf-8'))
        send_user_list()
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

receive()

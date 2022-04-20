import threading as t
import socket as s
import sys
import signal

host = '127.0.0.1'
port = 45500

users = []
clients = []

users_udp = []
add = []

thr_arr = []

server_tcp = s.socket(s.AF_INET, s.SOCK_STREAM)
server_tcp.bind((host, port))
print("Server_tcp initialized.")
server_tcp.listen()

server_udp = s.socket(s.AF_INET, s.SOCK_DGRAM)
server_udp.bind((host, port))
print("Server_udp initialized.")

def receive():
    while True:
        client, address = server_tcp.accept()
        client.send("Enter username".encode("utf-8"))
        user = client.recv(1024).decode("utf-8")
        clients.append(client)
        users.append(user)
        print(f"User {user} with address {address} has entered the chat.")
        broadcast_tcp(f"User {user} entered the chat.".encode("utf-8"))
        thread1 = t.Thread(target = handle_client_tcp, args = (client, ))
        thread2 = t.Thread(target = handle_client_udp, args = (user, ))
        thread1.daemon = True
        thread2.daemon = True
        thr_arr.append(thread1)
        thr_arr.append(thread2)
        thread1.start()
        thread2.start()

def broadcast_tcp(msg):
    for client in clients:
            client.send(msg)

def broadcast_udp(msg, sender):
    for address in add:
        if address != sender:
            server_udp.sendto(msg, address)

def handle_client_tcp(client):
    while True:
        try:
            msg = client.recv(1024).decode()
            i = clients.index(client)
            temp = users[i] + ": " + msg
            broadcast_tcp(temp.encode())
        except:
            i = clients.index(client)
            username = users[i]
            print(f"User {username} disconnected")
            if users[i] in users_udp:
                j = users_udp.index(users[i])
                users_udp.remove(users_udp[j])
                add.remove(add[j])
            clients.remove(client)
            users.remove(users[i])
            client.close()
            broadcast_tcp(f"User {username} has left the chat.".encode("utf-8"))
            break

def handle_client_udp(user):
    while True:
        buff, address = server_udp.recvfrom(4096)
        add.append(address)
        users_udp.append(user)
        temp_msg = user + ": \n" + str(buff, "utf-8")
        buff = bytes(temp_msg, "utf-8")
        broadcast_udp(buff, address)


def signal_handler(signal, frame):
    print("exiting")
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)

    thread0 = t.Thread(target = receive)
    thr_arr.append(thread0)
    thread0.daemon = True
    thread0.start()

    for thr in thr_arr:
        thr.join()
import socket as s
import threading as t
import sys
import signal
import struct

name = []

MULTICAST_GROUP = "224.1.1.1"
MULTICAST_PORT = 5004

client_tcp = s.socket(s.AF_INET, s.SOCK_STREAM)
client_tcp.connect(("127.0.0.1", 45500))

client_udp = s.socket(s.AF_INET, s.SOCK_DGRAM)

multicast_sender = s.socket(s.AF_INET, s.SOCK_DGRAM, s.IPPROTO_UDP)
multicast_sender.setsockopt(s.IPPROTO_IP, s.IP_MULTICAST_TTL, 2)

multicast_receiver = s.socket(s.AF_INET, s.SOCK_DGRAM, s.IPPROTO_UDP)
multicast_receiver.setsockopt(s.SOL_SOCKET, s.SO_REUSEADDR, 1)  
multicast_receiver.bind(('', MULTICAST_PORT))
mreq = struct.pack("4sl", s.inet_aton(MULTICAST_GROUP), s.INADDR_ANY)
multicast_receiver.setsockopt(s.IPPROTO_IP, s.IP_ADD_MEMBERSHIP, mreq)

thr_arr = []

def receive():
    while True:
        try:
            msg = client_tcp.recv(1024).decode("utf-8")
            if msg == "Enter username":
                print("Enter username: ")
                username = input()
                name.append(username)
                client_tcp.send(username.encode("utf-8"))
                thread3 = t.Thread(target = send)
                thr_arr.append(thread3)
                thread3.daemon = True
                thread3.start()
            else:
                print(msg)
        except:
            client_tcp.close()
            print("Unexpected error. Connection lost.")
            break

def receive_udp():
    while True:
        buff, address = client_udp.recvfrom(4096)
        print(str(buff, 'utf-8'))


def receiver_multicast():
    while True:
        buff, address = multicast_receiver.recvfrom(4096)
        print(str(buff, 'utf-8'))


def send():
    while True:
        try:
            msg = input()
            if msg == '/exit':
                sys.exit(1)
            elif msg == 'U':
                text_file = open("./image.txt", "r")
                art = text_file.read()
                client_udp.sendto(bytes(art, "utf-8"), ("127.0.0.1", 45500))
            elif msg == 'M':
                text_file = open("./image.txt", "r")
                art = name[0] + ": \n" + text_file.read()
                multicast_sender.sendto(bytes(art, "utf-8"), (MULTICAST_GROUP, MULTICAST_PORT))
            else:
                client_tcp.send(msg.encode("utf-8"))
        except:
            client_tcp.close()
            print("Unexpected error. Connection lost.")
            break

def signal_handler(signal, frame):
    print("\nexiting")
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    
    thread1 = t.Thread(target = receive)
    thread2 = t.Thread(target = receive_udp)
    thread4 = t.Thread(target = receiver_multicast)

    thr_arr.append(thread1)
    thr_arr.append(thread2)
    thr_arr.append(thread4)

    thread1.daemon = True
    thread2.daemon = True
    thread4.daemon = True

    thread1.start()
    thread2.start()
    thread4.start()

    for thr in thr_arr:
        thr.join()

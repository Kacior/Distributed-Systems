import socket;

serverIP = "127.0.0.1"
serverPort = 9008
msg = "żółta gęś".encode("utf8")

print('PYTHON UDP CLIENT')
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.sendto(msg, (serverIP, serverPort))

while True:
    buff, address = client.recvfrom(1024)
    print("python udp server received msg: " + int.from_bytes(buff, byteorder='little')))




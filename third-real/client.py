from socket import *


serverName = "127.0.0.1"
serverPort = 10000

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

clientSocket.send("client".encode("utf-8"))

sentence = None
while sentence != "quit":
    modifiedSentence = clientSocket.recv(1024)

    print('From Server: ', modifiedSentence.decode())

clientSocket.close()

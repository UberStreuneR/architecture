from socket import *


serverName = "127.0.0.1"
serverPort = 10000

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

clientSocket.send("sender".encode("utf-8"))

sentence = None
while sentence != "quit":
    sentence = input('Input: ')
    clientSocket.send(sentence.encode())

clientSocket.close()

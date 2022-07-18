import socket

def serverStart(IP="127.0.0.1", port=9090):
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind((IP, port))
    return serverSocket

def serverWaitForClient(serverSocket):
    serverSocket.listen()
    (clientConnected, clientAddress) = serverSocket.accept()
    print("connection attempt")
    return (clientConnected, clientAddress)

def clientConnect(IP="127.0.0.1", port=9090):
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.connect((IP, port))
    return clientSocket

def sendTo(data, connection):
    connection.send(data.encode())

def recieveFrom(connection):
    data = connection.recv(1024)
    return data.decode()


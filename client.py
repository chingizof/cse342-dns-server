import socket


def main():
    serverName = 'localhost'
    serverPort = 53

    clientSocket = socket(AF_INET, SOCK_DGRAM)

    message = input('Input lowercase sentence:') 

    # Send encoded message to server
    clientSocket.sendto(message.encode(),
                        (serverName, serverPort))
    
    # Receive message from server
    modifiedMessage, serverAddress = clientSocket.recvfrom(2048)

    # Print message from server
    print(modifiedMessage.decode())
    clientSocket.close()
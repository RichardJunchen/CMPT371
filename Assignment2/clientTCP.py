from socket import *
serverName = 'localhost'
serverPort = 50007
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect( (serverName, serverPort) )
print ("connected to: " + str(serverName) + str(serverPort) )
sentence = input('Input lowerecase sentence:')
clientSocket.send(sentence.encode())
modifiedSentence = clientSocket.recv(1024)
print( "From Server: " + modifiedSentence.decode())


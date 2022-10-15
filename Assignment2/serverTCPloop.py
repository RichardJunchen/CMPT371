import sys
print (sys.version)
from socket import *
serverHost = ''
serverPort = 50007
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(( serverHost, serverPort))
serverSocket.listen(1)
print ( 'The server is ready to receive ' )
while True:
	connectionID, addr = serverSocket.accept()
	print ("The server connected to: " + str(addr) )
	while True:
		sentence = connectionID.recv(1024).decode()
		if( sentence == "stop client" ): break
		if( sentence == "stop both" ): break
		print ("Message received: " + str(sentence ))
		capitalizedSentence = sentence.upper()
		print ("upcased: " + str(capitalizedSentence ))
		connectionID.send(capitalizedSentence.encode())
	connectionID.close()
	if( sentence == "stop both"): break
serverSocket.close()

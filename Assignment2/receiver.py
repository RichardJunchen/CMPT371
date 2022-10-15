# UDP SERVER
#REFERENCES:
#https://docs.python.org/2/library/ast.html
#https://docs.python.org/2/library/random.html
#https://docs.python.org/3/library/socket.html
import ast
import sys
import pickle
from random import *
print (sys.version)
from socket import *

seed_for_random = int(input("\n The seed for the random number generator used for determining if packet is CORRUPTED:  "))
probability = float(input("The probability that PACKET has been corrupted. Between [0 and 1) = "))
seed(seed_for_random)
#receiver create
serverHost = "127.0.0.1"
serverPort = 50007
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(( serverHost, serverPort))    #associates port to have certain properties

corrupted = False
dupcheck = [2,2]
swap = 0

###FUNCTIONS###
def rCheckAck(bigSeed):
	value = uniform(0.0,1.0)
	return value

def flipACKNACK():
	if corrupted == False:	#ACK == 1
		fieldlist[2] = 1
		fieldlist[3] = 0
	elif corrupted == True:	#NACK == 1
		fieldlist[2] = 0
		fieldlist[3] = 1
	fieldlist[0] = 0

def swapval():
	global swap
	if swap == 0:
		swap = 1
	else:
		swap = 0
def duplicate(list):
	isDup = False
	if(dupcheck[0] == dupcheck[1]):
		isDup = True
	return isDup
###############

print ( 'The server is ready to receive ' )
print('\n')

while True:
		sentence, clientAddress = serverSocket.recvfrom(1024) #packet data is in sentence, source addr is in clientAddress
		print ("Message received: " , sentence )
		capitalizedSentence = sentence.decode()
		fieldlist = ast.literal_eval(capitalizedSentence)   #turns list of type string back into a regular list
		# print("Fouse one here" + str(fieldlist))			# fieldlist containt same stuff as sentence (not same type)
		checkCorrupt = rCheckAck(seed_for_random)
		if checkCorrupt < float(probability):
			corrupted = True
		else:
			corrupted = False
				
		print('\n')


		# fieldlist = [data,seq,ack,nack]
		if corrupted == False:		#uncorrupted packet has been received
			print("Packet recieved contains : data = "+str(fieldlist[0])+" seq = "+str(fieldlist[1])+" isack = "+str(fieldlist[2])+" ack = "+str(fieldlist[3]) )
			flipACKNACK()
			if fieldlist[1] == 0:
				print("The receiver is moving to state WAIT FOR CALL 1 FROM BELOW")
				dupcheck[swap] = 0
				swapval()
				if(duplicate(dupcheck) == True):
					print("A duplicate packet with sequence number "+str(fieldlist[1])+" has been received")
				print("A packet with sequence number "+str(fieldlist[1])+" has been received")
			elif fieldlist[1] == 1:
				print("The receiver is moving to state WAIT FOR CALL 0 FROM BELOW")
				dupcheck[swap] = 1
				swapval()
				if(duplicate(dupcheck) == True):
					print("A duplicate packet with sequence number "+str(fieldlist[1])+" has been received")
				print("A packet with sequence number "+str(fieldlist[1])+" has been received")
			
			if fieldlist[2] == 1:
				state = "True"
			else: 
				state = "False"
			print("An ACK" + str(fieldlist[3]) +" is about to be sent")
			print("Packet to send contains: data = "+str(fieldlist[0])+" seq = "+str(fieldlist[1])+" isack = " + state +" ack = "+str(fieldlist[3]) )




		if corrupted == True:	#corrupted packet
			print("A Corrupted packet has just been received")

			flipACKNACK()
			if fieldlist[1] == 1:
				print("The receiver is moving back to state WAIT FOR CALL 0 FROM BELOW")
			print("The receiver is moving back to state WAIT FOR CALL 1 FROM BELOW")

			print("An ACK" + str(fieldlist[3]) +" is about to be sent")


			if fieldlist[2] == 1:
				state_2 = "True"
			else:
				state_2 = "False"
			
			print("Packet to send contains: data = "+str(fieldlist[0])+" seq = "+str(fieldlist[1])+" isack = " + state_2 +" ack = "+str(fieldlist[3]) )			



		print('\n')
		capitalizedSentence = str(fieldlist)
		print(capitalizedSentence)
		serverSocket.sendto(capitalizedSentence.encode(), clientAddress)


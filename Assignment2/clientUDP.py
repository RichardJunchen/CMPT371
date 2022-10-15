from socket import *
from time import *
from random import *
import random
import ast


#PACKET_CREATOR
def makepkt(field2_sequence_packet,field4_sequence_ACK):
	field1 = randint(0, 4294967296)  #32 bit integer - 2^31 <= n < 2^31
	field3_ACK = 1   #Packet contents for an ACK or NACK packets is 0 
	packet = [field1, field2_sequence_packet, field3_ACK, field4_sequence_ACK]
	return packet



#random_number_generator
def random_number_generator(start,end):
    random_number = random.uniform(start,end)
    return random_number


#SOCKET CREATED
serverName = 'localhost'
serverPort = 50007
clientSocket = socket(AF_INET, SOCK_DGRAM)


#Read the values of the following quantities
seed_for_timing = int(input(" Please enter the seed for the random number generator used for TIMING: "))
print("\n")
number_of_packets = int(input(" Please enter the number of packets you will send: "))
print("\n")
seed_for_ACK = int(input(" Please enter the seed for random number generator for determing if ACKs have been CORRUPTED: "))
print("\n")
probability = float(input(" Please enter the PROBABILITY that an ACK has been corrupted !!A float between [0 ~ 1]!! : "))
print("\n")
travel_time = float(input(" Please enter the ROUND TRIP TRAVEL TIME for ACK : "))
print("\n")
random.seed(seed_for_timing)

sequence_for_packet = 0
sequence_for_ACK = 0
count = 0

#MAIN PROCESS OF SENDING THE PACKETS
while count < number_of_packets:
    packet = makepkt(sequence_for_packet,sequence_for_ACK)

    current_time = time()
    expected_arrival_time = current_time


#Print three messages immediately before a packet is sent.

    print('\nA packet with sequence number  ' + str(sequence_for_packet) + '  about to be sent')

    if packet[2] == 1:
        state = "True"
    else: 
        state = "False"

    print('Packet to send contains:  data = ' +  str(packet[0]) + ' seq = ' +  str(packet[1]) + ' isack = ' + state +' ack = ' + str(packet[3]))
    
    print('Starting timer for ACK' + str(packet[3]))


    clientSocket.sendto( str(packet).encode(), (serverName, serverPort))
    random_delay_number = float(random_number_generator(0.0,5.0))
    expected_arrival_time = expected_arrival_time + travel_time + random_delay_number 

	
    current = time()
    if current < expected_arrival_time:
	    difference = expected_arrival_time - current
	    sleep(difference)

    print ('Message sent')
    print('\nThe sender is moving to state WAIT FOR ACK' + str(packet[3]) +'\n')

    try:
        current > expected_arrival_time
    except:
        print(" ACK" + str(packet[3]) + " timer expired"+'\n')
        

    try:
        clientSocket.settimeout(float(travel_time))
        modifiedMessage, severAddress = clientSocket.recvfrom(2048)
    # print("!!!!!!!!!!" + str(modifiedMessage.decode))
        packet_received = ast.literal_eval(modifiedMessage.decode())
    # print("!!!!!!!!!!" + str(packet_received))
        clientSocket.settimeout(None)

        if packet_received[2] == 0:
            print(" ACK" + str(packet[3]) + " timer expired"+'\n')

    
	
#random() to generate random number that will be used to determine if an ACK that has just arrived has been corrupted.
        random_number_for_ACK = random_number_generator(0.0,1.0)

# the ACK packet is corrupted
        if random_number_for_ACK < probability:
        # print("random = " + str(random_number_for_ACK)+ "," + "prob = " + str(probability))

            print('A Corrupted ACK packet has just been received')

            if sequence_for_packet == 0:
                print('\nThe sender is moving back to state WAIT FOR CALL 0 FROM ABOVE \n')
            else:
                print('\nThe sender is moving back to state WAIT FOR CALL 1 FROM ABOVE\n')
# the ACK packet is uncorrupted
        else:
        # print("random = " + str(random_number_for_ACK)+ "," + "prob = " + str(probability))

            print('An ACK' + str(packet_received[3]) + ' packet has just been received')
		
            if packet_received[2] == 1:
                state_2 = "True"
            else: 
                state_2 = "False"

            print('Packet received contains: data = ' + str(packet_received[0]) + ' seq = '  + str(packet_received[1]) + ' isack = ' + state_2 +' ack = ' +  str(packet_received[3]) + '\n')

            print('Stopping timer for ACK' + str(packet[3]))

            if sequence_for_packet == 0:
                print('\nThe sender is moving to state WAIT FOR CALL 1 FROM ABOVE \n')
            else:
                print('\nThe sender is moving to state WAIT FOR CALL 0 FROM ABOVE \n')
    
    except timeout as e:
        print(" ACK" + str(packet[3]) + " timer expired"+'\n')
        print('A packet with sequence number  ' + str(sequence_for_packet) + 'is about to be resent')
        clientSocket.sendto( str(packet).encode(), (serverName, serverPort))   
    print("--------------------------------------------------------------------------")


    sequence_for_packet = 1 - sequence_for_packet
    sequence_for_ACK = 1 - sequence_for_ACK
    count += 1


#SOCKET CLOSED
clientSocket.close()
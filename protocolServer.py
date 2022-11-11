#Dylan Dockery
#Server to process custom protocol and print out payload as buffer. Checks for data integrity and rerequests packet if corrupt
#libraries needed : socket, argparse, random
#instructions: 
#Start via commandline. Commandline parameters are as follows:
#-p --- Port used for server. Required 

from socket import *
import argparse
import random

#checks the integretiy of the pack by recalculating checksum and comparing
def integrityCheck(message):
    #partition packet into header and message snas check sum and message
    headerLength=8
    checkByte1=8
    checkByte2=9
    messageIndex=10
    packet_header=message[0:headerLength]
    packet_message=message[messageIndex:]

    check_sum1 = 0
    check_sum2 = 0

    for i in range(0,len(packet_header),2):
        check_sum1=check_sum1^packet_header[i]
        check_sum2=check_sum2^packet_header[i+1]

    for j in range(0,len(packet_message),2):
        check_sum1=check_sum1^packet_message[j]
        check_sum2=check_sum2^packet_message[j+1]

    if check_sum1 != message[checkByte1] or check_sum2 != message[checkByte2]:
        return True
    else:
        return False

#formats the packet in bytes Arguments: destination port, packet payload, protocol flag, sequence number
def encode(port, message,flag):
    flagIndex=7
    #packet
    packet=bytearray()
    #protocol identifier
    packet.append(1)
    #packet length
    packet.append(10)
    #port number stored in 2 bytes
    port_bytes=port.to_bytes(2,'big')
    packet.append(port_bytes[0])
    packet.append(port_bytes[1])

    #random integer stored in 2 bytes
    random_int=random.randrange(0, 65535, 1).to_bytes(2,'big')
    packet.append(random_int[0])
    packet.append(random_int[1])
    #response flag
    packet.append(flag)
    #sequence number
    packet.append(message[flagIndex])
    
    #check sum calculation then stored as 2 bytes at end of header 
    check_sum1 = 0
    check_sum2 = 0
    
    for i in range(0,len(packet),2):
        check_sum1=check_sum1^packet[i]
        check_sum2=check_sum2^packet[i+1]

    packet.append(check_sum1)
    packet.append(check_sum2)

    return packet

#decodes message from received packet   
def decode(message):
    return message[10:message[1]].decode('utf-8')


#command line argmuent declaration
parser = argparse.ArgumentParser(description='Server')
parser.add_argument('-p', type=int, default=8000,help='Port used for server. Required', required=True)
args = parser.parse_args()
port = args.p

#protocol numbers
ACK=1
NACK=2

serverSocket = socket(AF_INET,SOCK_DGRAM)
serverSocket.bind(('',port))
print("The server is ready to receive")

#data store
data=""
while True:
    message, clientAddress = serverSocket.recvfrom(2048)
    if message[0]==0:
        flag=ACK
        if integrityCheck(message):
            flag=NACK
        else:
            data=data+decode(message)
            print(data)
        response = encode(clientAddress[1],message, flag)
        serverSocket.sendto(response,clientAddress)
        
        
        


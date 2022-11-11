#Dylan Dockery
#Client to generate message and send it using a custom protocol. 
#libraries needed : socket, argparse, random
#instructions: 
#Start via commandline. Commandline parameters are as follows:
#-p --- Port used for server. Required 
#-m --- Message to be send via UDP with custom protocol

from socket import *
import argparse
import random

#formats the packet in bytes Arguments: destination port, packet payload, protocol flag, sequence number
def encode(port, message,flag,seq):
    #packet
    protocol_header=bytearray()
    #protocol identifier
    protocol_header.append(0)
    #length of packet
    protocol_header.append((len(message)+10))
    #port and 2 bytes ro store it 
    port_bytes=port.to_bytes(2,'big')
    protocol_header.append(port_bytes[0])
    protocol_header.append(port_bytes[1])
    #random integer and 2 bytes to store it
    random_int=random.randrange(0, 65535, 1).to_bytes(2,'big')
    protocol_header.append(random_int[0])
    protocol_header.append(random_int[1])
    #protocol flag
    protocol_header.append(flag)
    #sequnece number
    protocol_header.append(seq)
    
    #if packet payload is less then 8 characters pad with 0s then encode as bytes
    if len(message)%8 != 0:
        message = message + '0' * (8-len(message)%8)
    protocol_message=message.encode('utf-8')

    #check sum calculation then stored as 2 bytes at end of header 
    check_sum1 = 0
    check_sum2 = 0
    
    for i in range(0,len(protocol_header),2):
        check_sum1=check_sum1^protocol_header[i]
        check_sum2=check_sum2^protocol_header[i+1]

    for j in range(0,len(protocol_message),2):
        check_sum1=check_sum1^protocol_message[j]
        check_sum2=check_sum2^protocol_message[j+1]
    protocol_header.append(check_sum1)
    protocol_header.append(check_sum2)

    #merge header and payload and return as packet
    packet=protocol_header+protocol_message
    return packet
    
#corrupts random byte of packet bar the first idnetifier byte
def corrurpPacket(packet):
    packet[random.randrange(1, 18, 1)]=random.randrange(0, 255, 1)
    return packet

#command line argmuent declaration
parser = argparse.ArgumentParser(description='Server')
parser.add_argument('-i', type=str, default='127.0.0.1',help='IP address for server Default is 127.0.0.1')
parser.add_argument('-p', type=int, help='Port used for server. Required', required=True)
parser.add_argument('-m', type=str,help='Message to be sent to server', required=True)
args = parser.parse_args()
message = args.m
ip_addr = args.i
port = args.p

#protocol variables
SND=0
ACK=1
NACK=2
#initial sequence number
seq=1

#partition message longer than 8 characters into payloads of sixe 8 or less
payloads = [message[start:start+8] for start in range(0,len(message),8)]

#send each payload across UDP connection
for p in payloads:
    packet = encode(port,p,SND,seq)

    #1 in 10 chance to corrupt packet
    corrupt_flag=random.randrange(0, 10, 1)
    if corrupt_flag == 1:
        packet=corrurpPacket(packet)
    clientSocket = socket(AF_INET,SOCK_DGRAM)
    clientSocket.sendto(packet,(ip_addr,port))
    response, serverAddress=clientSocket.recvfrom(2048)
    #resend packet until ACK
    while(response[6]==NACK):
        packet = encode(port,p,SND,seq)
        clientSocket.sendto(packet,(ip_addr,port))
        response, serverAddress=clientSocket.recvfrom(2048)
        print(packet)
    #flip sequence numebr 
    seq=response[7]^1



#Dylan Dockery
#Server to process HTTP GET requests
#libraries needed : socket, argparse
#instructions: 
#Start via commandline. Commandline parameters are as follows:
#-p --- Port used for server. Required 

from socket import *
import argparse
import random

def encode(port, message,flag,seq):
    protocol_header=bytearray()
    protocol_header.append(1)
    protocol_header.append((len(message)+10))
    port_bytes=port.to_bytes(2,'big')
    protocol_header.append(port_bytes[0])
    protocol_header.append(port_bytes[1])
    random_int=random.randrange(0, 65535, 1).to_bytes(2,'big')
    protocol_header.append(random_int[0])
    protocol_header.append(random_int[1])
    protocol_header.append(flag)
    protocol_header.append(seq)
    
    protocol_message=message.encode('utf-8')

    print(protocol_header)
    print(protocol_message)
    check_sum = 0
    for i in protocol_header:
        check_sum=check_sum^i

    for j in protocol_message:
        check_sum=check_sum^i

    protocol_header.append(check_sum)
    packet=protocol_header+protocol_message
    for k in packet:
        print(k)

#command line argmuent declaration
parser = argparse.ArgumentParser(description='Server')
parser.add_argument('-i', type=str, default='127.0.0.1',help='IP address for server Default is 127.0.0.1')
parser.add_argument('-p', type=int, default=8000,help='Port used for server. Required', required=True)
parser.add_argument('-m', type=str,help='Message to be sent to serverr', required=True)
args = parser.parse_args()
encode(args.p,args.m,1,1)
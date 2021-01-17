# -*- coding: utf-8 -*-
"""
Created on Tue Aug 18 18:38:07 2020

@author: Berkay
"""

import sys
import socket

try:
    ms = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except:
    print("FAILED TO CREATE A SOCKET")
    sys.exit()


    
try:
    ms.connect(("192.168.1.10", 80))
except:
    print("FAILED TO CONNECT TO THE SERVER") 
    sys.exit()

    
while True:    
    message = input("Enter the message you want to send(exit to disconect):")
    data = message.encode()
    
    try:
        ms.sendall(data)    
    except:
        print("FAILED TO SEND THE REQUEST")
        sys.exit()
    data = ms.recv(1000).decode()
    if data == '':
        print("Connection lost!")
        sys.exit()
    print("Data received is:\n" + data)   
    

ms.close()    


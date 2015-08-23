'''
Created on 17 Aug 2015

@author: andy
'''

import socket
import threading

S = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
S.connect(('localhost', 9999))

def read_data():
    """."""
    print('STARTED READ')
    while True:
        data = S.recv(1024)
        if data:
            print('RECEIVED: ' + data.decode('utf-8'))

def send_data():
    """."""
    print('STARTED SEND')
    while True:
        intxt = input()
        S.send(intxt.encode('utf-8'))
        print('SENT: ' + intxt)


if __name__ == '__main__':
    THREAD1 = threading.Thread(target=read_data)
    THREAD1.start()
    THREAD2 = threading.Thread(target=send_data)
    THREAD2.start()

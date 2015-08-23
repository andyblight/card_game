'''
Created on 17 Aug 2015

@author: andy
'''

import socketserver

class MyTCPHandler(socketserver.BaseRequestHandler):
    """."""
    def handle(self):
        """."""
        iterations = 0
        while iterations < 20:
            received_data = self.request.recv(1024)
            received_string = received_data.decode('utf8')
            if not received_string:
                print('DISCONNECTED')
                break
            print('RECEIVED: ', received_string, iterations)
            self.request.sendall(received_string[::-1].encode('utf-8'))
            iterations += 1

if __name__ == '__main__':
    SERVER = socketserver.TCPServer(('localhost', 9999), MyTCPHandler)
    SERVER.serve_forever()

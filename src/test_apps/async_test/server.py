#! /usr/bin/python3
"""
Allows one telnet client to connect using:
 telnet localhost 2222

Created on 19 Aug 2015 from
http://www.drdobbs.com/open-source/the-new-asyncio-in-python-34-servers-pro/240168408
with PyLint fixes.
"""

import asyncio

class SimpleEchoProtocol(asyncio.Protocol):
    """Echoes back data sent from a telnet client."""
    def __init__(self):
        self.transport = None

    def connection_made(self, transport):
        """
        Called when a connection is made.
        The argument is the transport representing the pipe connection.
        To receive data, wait for data_received() calls.
        When the connection is closed, connection_lost() is called.
        """
        print("Connection received!")
        self.transport = transport

    def data_received(self, data):
        """
        Called when some data is received.
        The argument is a bytes object.
        """
        print(data)
        self.transport.write(b'echo:')
        self.transport.write(data)

    def connection_lost(self, exc):
        """
        Called when the connection is lost or closed.
        The argument is an exception object or None (the latter
        meaning a regular EOF is received or the connection was
        aborted or closed).
        """
        print("Connection lost! Closing server...")
        SERVER.close()

if __name__ == '__main__':
    LOOP = asyncio.get_event_loop()
    SERVER = LOOP.run_until_complete(LOOP.create_server(SimpleEchoProtocol,
                                                        'localhost', 2222))
    LOOP.run_until_complete(SERVER.wait_closed())

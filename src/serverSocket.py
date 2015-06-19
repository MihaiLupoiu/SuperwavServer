__author__ = 'mihai'
import socket
import select
import sys

CONNECTION_LIST = []    # list of socket clients
RECV_BUFFER = 4096 # Advisable to keep it as an exponent of 2

def startServerConfiguration(PORT):

    # Create a TCP/IP socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setblocking(0)


    # Bind the socket to the port
    server_address = ('localhost', PORT)
    print >>sys.stderr, 'starting up on %s port %s' % server_address
    server.bind(server_address)

    # Listen for incoming connections
    server.listen(30)

    # Add server socket to the list of readable connections
    CONNECTION_LIST.append(server)

    print "Server started on port " + str(PORT)

    return server

def startServerConnection(PORT):

    server = startServerConfiguration(PORT)
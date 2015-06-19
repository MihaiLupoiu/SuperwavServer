__author__ = 'mihai'
import socket
import select
import sys

def startServerConnection(PORT):
    # Create a TCP/IP socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setblocking(0)


    # Bind the socket to the port
    server_address = ('localhost', PORT)
    print >>sys.stderr, 'starting up on %s port %s' % server_address
    server.bind(server_address)

    # Listen for incoming connections
    server.listen(30)






    CONNECTION_LIST = []    # list of socket clients
    RECV_BUFFER = 4096 # Advisable to keep it as an exponent of 2
    PORT = 4444

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # this has no effect, why ?
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("0.0.0.0", PORT))
    server_socket.listen(30)

    # Add server socket to the list of readable connections
    CONNECTION_LIST.append(server_socket)

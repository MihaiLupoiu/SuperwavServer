__author__ = 'mihai'
import socket
import select
import sys
import Queue
import time

import termios, fcntl, os

from threading import Thread, Lock


RECV_BUFFER = 4096 # Advisable to keep it as an exponent of 2

def startServerConfiguration(PORT):

    # Create a TCP/IP socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setblocking(0)


    # Bind the socket to the port
    server_address = ('localhost', PORT)
    print >>sys.stderr, 'Starting up on: %s port: %s' % server_address
    server.bind(server_address)

    # Listen for incoming connections
    server.listen(30)

    # Sockets from which we expect to read
    inputs = [ server ]

    # Sockets to which we expect to write
    outputs = [ ]

    # Outgoing message queues (socket:Queue)
    message_queues = {}

    print "Server started on port " + str(PORT)

    return (server,inputs,outputs,message_queues)

def get_char_keyboard_nonblock():
    fd = sys.stdin.fileno()

    oldterm = termios.tcgetattr(fd)
    newattr = termios.tcgetattr(fd)
    newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
    termios.tcsetattr(fd, termios.TCSANOW, newattr)

    oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)
    fcntl.fcntl(fd, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)

    c = None

    try:
        c = sys.stdin.read(1)
    except IOError: pass

    termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
    fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)

    return c

def notifyClients(clientsList, timeStamp, idClient,message_queues,outputs):
    send = "StartTime: "+str(timeStamp)+", IDClient: "+str(idClient)
    print send
    for client in clientsList:
        message_queues[client].put(send)
        if client not in outputs:
            outputs.append(client)

def startServerConnection(PORT):

    numberOfCLients = 1;
    server,inputs,outputs,message_queues = startServerConfiguration(PORT)

    searchBool = True
    playingBool = False

    exitToken = False
    run = True

    while run:
        # Wait for at least one of the sockets to be ready for processing print >>sys.stderr, '\nwaiting for the next event'
        timeout = 1
        readable, writable, exceptional = select.select(inputs, outputs, inputs, timeout)

        if not (readable or writable or exceptional):
            #print >>sys.stderr, '  Timed out, do some other work here'
            char = get_char_keyboard_nonblock()
            if char != None:
                print char
                if char == 's':
                    if playingBool:
                        print >>sys.stderr, '  Player already running, it will not inicialize.'
                    else:
                        searchBool = False
                        playingBool = True
                        print >>sys.stderr, '  Music will start in 10 seconds!'

                        timeStamp = int(time.time()*1000)
                        timeToSend = timeStamp + (10 *1000)

                        #notifyClients
                        notifyClients(inputs[1:], timeToSend, 1, message_queues,outputs)

                if char == 'p':
                    try:
                        clientToPlay = int(raw_input("Please enter a number: "))
                    except ValueError:
                        print "Oops!  That was no valid number.  Try again..."

                    notifyClients(inputs[1:], 0, clientToPlay, message_queues,outputs)

                if char == 'e':
                    notifyClients(inputs[1:], 0, -1, message_queues,outputs)
                    exitToken = True
            continue
        print "HOLA...\n"
        if searchBool == True:
            # Handle inputs
            for s in readable:
                if s is server:
                    # A "readable" server socket is ready to accept a connection
                    connection, client_address = s.accept()
                    print >>sys.stderr, 'New connection from', client_address
                    connection.setblocking(0)
                    inputs.append(connection)

                    # Give the connection a queue for data we want to send
                    message_queues[connection] = Queue.Queue()

                    message_queues[connection].put(str(numberOfCLients))
                    if connection not in outputs:
                        outputs.append(connection)

                    numberOfCLients += 1

                else:
                    data = s.recv(1024)
                    if data:
                        # A readable client socket has data
                        print >>sys.stderr, 'Received "%s" from %s' % (data, s.getpeername())

                        #Respond client
#                        message_queues[s].put(data)
                        # Add output channel for response
#                        if s not in outputs:
#                            outputs.append(s)
                    else:
                        # Interpret empty result as closed connection
                        print >>sys.stderr, 'Closing', client_address, 'after reading no data'
                        # Stop listening for input on the connection
                        if s in outputs:
                            outputs.remove(s)
                        inputs.remove(s)
                        s.close()

                        # Remove message queue
                        del message_queues[s]

        # Handle outputs
        for s in writable:
            try:
                next_msg = message_queues[s].get_nowait()
            except Queue.Empty:
                # No messages waiting so stop checking for writability.
                print >>sys.stderr, 'Output queue for', s.getpeername(), 'is empty'
                outputs.remove(s)
                if exitToken:
                    run = False
            else:
                print >>sys.stderr, 'Sending "%s" to %s' % (next_msg, s.getpeername())
                s.send(next_msg)

    print "Server is closing."
    server.close()
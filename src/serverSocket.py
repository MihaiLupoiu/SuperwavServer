__author__ = 'mihai'
import socket
import select
import sys
import Queue
import time
import termios, fcntl, os  # For reading keyboard imput
from config import readConfigFile  # For reading config file

RECV_BUFFER = 4096  # Advisable to keep it as an exponent of 2


def startServerConfiguration(port, clients_number):
    """

    :rtype : Socket Server, list of inputs, list of outputs, list of messages_queue
    """
    # Create a TCP/IP socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setblocking(0)


    # Bind the socket to the port
    server_address = ('', port)
    print >> sys.stderr, 'Starting up on: %s port: %s' % server_address
    server.bind(server_address)

    # Listen for incoming connections
    server.listen(clients_number)

    # Sockets from which we expect to read
    inputs = [server]

    # Sockets to which we expect to write
    outputs = []

    # Outgoing message queues (socket:Queue)
    message_queues = {}

    return server, inputs, outputs, message_queues


def get_char_keyboard_nonblock():
    """

    :rtype : char
    """
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
    except IOError:
        pass

    termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
    fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)

    return c


def notifyClients(clients_list, message_queues, outputs, message_to_send):
    """

    :rtype : void
    """
    for client in clients_list:
        message_queues[client].put(message_to_send)
        if client not in outputs:
            outputs.append(client)


def notifyOneClient(client, message_queues, outputs, message_to_send):
    """

    :rtype : void
    """
    notifyClients([client], message_queues, outputs, message_to_send)


def notifyClientsFlag(clients_list, time_stamp, id_client, message_queues, outputs):
    """

    :rtype : void
    """
    message_to_send = "Action:flag,StartTime:" + str(time_stamp) + ",IDClient:" + str(id_client)
    notifyClients(clients_list, message_queues, outputs, message_to_send)


def notifyClientsClientPos(clients_list, time_stamp, client_pos, message_queues, outputs):
    """

    :rtype : void
    """
    message_to_send = "Action:client,StartTime:" + str(time_stamp) + ",ClientPosX:" + str(client_pos[0]) + ",ClientPosY:" + str(
        client_pos[1])
    notifyClients(clients_list, message_queues, outputs, message_to_send)


def notifyClientsSongsPos(clients_list, time_stamp, song, song_pos, message_queues, outputs):
    """

    :rtype : void
    """
    message_to_send = "Action:song,StartTime:" + str(time_stamp) + ",Song:" + str(song) + ",SongPosX:" + str(
        song_pos[0]) + ",SongPosY:" + str(song_pos[1])
    notifyClients(clients_list, message_queues, outputs, message_to_send)


def startServerConnection(PORT):
    config_file = readConfigFile()

    number_of_clients = 1
    server, inputs, outputs, message_queues = startServerConfiguration(PORT, config_file.clients_number)

    search_bool = True
    playing_bool = False

    exit_token = False
    run = True

    timeout = 1

    while run:
        # Wait for at least one of the sockets to be ready for
        # processing print >>sys.stderr, '\nwaiting for the next event'
        readable, writable, exceptional = select.select(inputs, outputs, inputs, timeout)

        if not (readable or writable or exceptional):
            # print >>sys.stderr, '  Timed out, do some other work here'
            char = get_char_keyboard_nonblock()
            if char is not None:
                if char == 's':
                    if playing_bool:
                        print >> sys.stderr, '  Player already running, it will not inicialize.'
                    else:
                        search_bool = False
                        playing_bool = True
                        print >> sys.stdout, '  Music will start in ' + str(config_file.time_to_start) + ' seconds!'

                        time_stamp = int(time.time() * 1000)
                        time_to_send = time_stamp + (config_file.time_to_start * 1000)

                        message_to_send = "Action:start,StartTime:" + str(time_to_send) + ",ClientPosX:" + \
                                          str(config_file.clientPos[0]) + ",ClientPosY:" + \
                                          str(config_file.clientPos[1]) + ",Song:" + str(-1) + ",SongPosX:" + \
                                          str(config_file.inicialSongPos[0]) + ",SongPosY:" + str(
                            config_file.inicialSongPos[1])

                        notifyClients(inputs[1:], message_queues, outputs, message_to_send)

                if char == 'p':
                    try:
                        client_to_play = int(raw_input("Please enter a client number: "))
                        notifyClientsFlag(inputs[1:], 0, client_to_play, message_queues, outputs)

                    except ValueError:
                        server.close()
                        print >> sys.stderr, '  Oops!  That was no valid number.  Try again...'

                if char == 'c':
                    try:
                        client_pos_x = int(raw_input("Please enter a client position X: "))
                        client_pos_y = int(raw_input("Please enter a client position Y: "))
                        notifyClientsClientPos(inputs[1:], 0, (client_pos_x, client_pos_y), message_queues, outputs)

                    except ValueError:
                        server.close()
                        print >> sys.stderr, '  Oops!  That was no valid number.  Try again...'

                if char == 'f':
                    try:
                        print >> sys.stdout, '  Select one of the next %s songs to change position: ' % str(
                            config_file.number_sounds)
                        cont = 0
                        for songPos in config_file.Sound_List_Pos:
                            print >> sys.stdout, cont, songPos[0]  # , songPos[1][0], songPos[1][1]
                            cont += 1

                        selected_song = int(raw_input("Select: "))
                        print >> sys.stdout, ' Selected: "%s"' % config_file.Sound_List_Pos[selected_song][0]

                        song_pos_x = int(raw_input("Please enter a position X: "))
                        song_pos_y = int(raw_input("Please enter a position Y: "))
                        notifyClientsSongsPos(inputs[1:], 0, selected_song, (song_pos_x, song_pos_y), message_queues,
                                              outputs)

                    except ValueError:
                        server.close()
                        print >> sys.stderr, '  Oops!  That was no valid number.  Try again...'

                if char == 'e':
                    # notifyClientsFlag(inputs[1:], 0, -1, message_queues, outputs)
                    notifyClients(inputs[1:], message_queues, outputs, "Action:exit")
                    exit_token = True
                    if len(inputs[1:]) == 0:
                        break
            continue

        if search_bool:
            # Handle inputs
            for s in readable:
                if s is server:
                    # A "readable" server socket is ready to accept a connection
                    connection, client_address = s.accept()
                    print >> sys.stdout, 'New connection from', client_address
                    connection.setblocking(0)
                    inputs.append(connection)

                    # Give the connection a queue for data we want to send
                    message_queues[connection] = Queue.Queue()

                    notifyOneClient(connection, message_queues, outputs, "Action:identification,ID:{0}".format(str(number_of_clients)))
                    number_of_clients += 1

                else:
                    data = s.recv(1024)
                    if data:
                        # A readable client socket has data
                        print >> sys.stdout, 'Received "%s" from %s' % (data, s.getpeername())

                        # Respond client
                        # message_queues[s].put(data)
                        # Add output channel for response
                        # if s not in outputs:
                        #   outputs.append(s)
                    else:
                        # Interpret empty result as closed connection
                        print >> sys.stderr, 'Closing', client_address, 'after reading no data'
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
                # print >> sys.stderr, 'Output queue for', s.getpeername(), 'is empty'
                outputs.remove(s)
                if exit_token:
                    run = False
            else:
                print >> sys.stdout, 'Sending "%s" to %s' % (next_msg, s.getpeername())
                s.send(next_msg)
    print "Server is closing."
    server.close()

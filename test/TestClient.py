__author__ = 'mihai'
import socket
import sys
import time

# Create a TCP/IP socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('localhost', 4444)
print >> sys.stderr, 'Starting up on: %s port: %s' % server_address
server.bind(server_address)

# Listen for incoming connections
server.listen(1)

connection, client_address = server.accept()
print >> sys.stdout, 'New connection from', client_address

time.sleep(3)

msg = "ID:1"
print msg
connection.send(msg)

time.sleep(3)

time_stamp = int(time.time() * 1000)
time_to_send = time_stamp + (10 * 1000)

print time_stamp
msg = "StartTime:%s,ClientPosX:6,ClientPosY:5,Song:-1,SongPosX:11,SongPosY:0" % time_to_send
print msg
connection.send(msg)

time.sleep(3)

msg = "StartTime:0,ClientPosX:7,ClientPosY:5"
print msg
connection.send(msg)

time.sleep(3)

msg = "StartTime:0,Song:1,SongPosX:5,SongPosY:0"
print msg
connection.send(msg)

msg = "Action:exit"
print msg
connection.send(msg)


connection.close()

server.close()
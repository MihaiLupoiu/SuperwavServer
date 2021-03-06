#!/usr/bin/env python
#http://pymotw.com/2/select/
__author__ = 'mihai'
import sys
from serverSocket import *

PORT = None

if __name__ == "__main__":

    try:
        print sys.argv[1]
        if sys.argv[1] == "-h":
            print("To use the program:\n As a Server:\n SuperWavAppServer <PortNumber>\n")
            exit(0)
        else:
            PORT = int(sys.argv[1])
            print("\n***********************\n Port Number: %s \n***********************\n" % str(PORT))

            startServerConnection(PORT)
    except:
        if len(sys.argv) < 2:
            print("Wrong use of the program! For help use -h option.\n")
        else:
            print "Unexpected error:", sys.exc_info()[0]
            raise
        exit(-1)


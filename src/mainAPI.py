__author__ = 'mihai'

# Threads leer:
# https://pyzone.wordpress.com/2008/02/05/threads-parte-ii/
from lib.bottle import run, post, request

@post("/SuperWAV/api")
def API():
    data = request.json
    print data


run(host='localhost', port=9090)
__author__ = 'mihai'

from lib.bottle import run, post, request

@post("/SuperWAV/api")
def API():
    data = request.json
    print data


run(host='localhost', port=9090)
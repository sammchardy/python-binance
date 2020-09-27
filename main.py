#!/usr/bin/python

import threading
import time
'''
# Define a function for the thread
def print_time( threadName, delay):
   count = 0
   while count < 5:
      time.sleep(delay)
      count += 1
      print "%s: %s" % ( threadName, time.ctime(time.time()) )

# Create two threads as follows
try:
   thread.start_new_thread( print_time, ("Thread-1", 2, ) )
   thread.start_new_thread( print_time, ("Thread-2", 4, ) )
except:
   print "Error: unable to start thread"

while 1:
   pass
'''
import socket  # for socket
import sys


def test1():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Socket successfully created")
    except socket.error as err:
        print("socket creation failed with error %s" % (err))

    # default port for socket
    port = 80

    try:
        host_ip = socket.gethostbyname('www.google.com')
    except socket.gaierror:

        # this means could not resolve the host
        print("there was an error resolving the host")
        sys.exit()

    # connecting to the server
    s.connect((host_ip, port))

    print("the socket has successfully connected to google \
    on port == %s" % (host_ip))


def test2():
    s = socket.socket()
    print("Socket successfully created")

    # reserve a port on your computer in our
    # case it is 12345 but it can be anything
    port = 12345

    # Next bind to the port
    # we have not typed any ip in the ip field
    # instead we have inputted an empty string
    # this makes the server listen to requests
    # coming from other computers on the network
    s.bind(('', port))
    print("socket binded to %s" % (port))

    # put the socket into listening mode
    s.listen(5)
    print("socket is listening")

    # a forever loop until we interrupt it or
    # an error occurs
    num = 0
    c, addr = s.accept()

    while True:
        # Establish connection with client.

    #    print('Got connection from', addr)

        # send a thank you message to the client.
        msg = bytes('Thank you for connecting, counting {0}'.format(num),'utf-8')
        c.send(msg)
        print(msg)
        print('sending: {0}'.format(num))
        # Close the connection with the client
        c.close()



test2()
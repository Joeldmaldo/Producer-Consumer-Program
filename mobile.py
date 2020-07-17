# Author: Joel Maldonado Rivera
# Student-ID: 801-14-3804
# H.W # 1 : Consumer and Producer problem



# We create the Mobile.py which will have one thread which will do the following:
#  1)Concurrently generate random numbers that simulates the time the mobile job will take in the compute server.
#  2) Send a message for each "job" to the compute server with a mobile ID.
#     Sleep a short (1 to 5 seconds) random period of time between sends.


# References for work:
"""
  1)https://docs.python.org/2/library/threading.html
  2)http://thomas-cokelaer.info/tutorials/python/module_threading.html
  3)https://pymotw.com/2/socket/udp.html
  4)https://www.networkcomputing.com/applications/python-network-programming-handling-socket-errors/1384050408
  5)https://www.8bitavenue.com/2016/11/python-mutex-example/
  6)https://self-learning-java-tutorial.blogspot.com/2015/12/python-bounded-semaphore.html
  """



# We import the modules we will be using:

import threading
import random
import sys 
import socket
import time
from random import randint
from threading import Thread


# we define our worker function:
# This function does the following:
#  1) It will generate how long each work created will "run" for.
#  2) It will store the given id and the time this id will run for in the "info" variable as a string
#  3) Afterwards it takes the given ip and port in order to create the serverAddress + it creates the socket 
#  4) We try to send the information we stored in the "info" variable through serverAddres(ip and port) variable.
#  5) Afterwards we wait for a reply from the server from the same port
#  6) If it occurs we then close the socket.

def worker():
    """thread worker function"""
    b = sys.argv
    time_var = random.randint(1,20)  # make the time the job will "run" from 1 sec to 20
    print( 'worker id: '+str(b[1])+ " work time: "  + str(time_var) + '\n')
    info= str(b[1]) +':' +str(time_var)
    host = b[2]#'127.0.1.1'
    port = b[3]
    port = int(port)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    serverAddress=(host,port)
    #Info will be the message sent

    try:
    	print("sending message info")
    	sent= sock.sendto(info,serverAddress)
    except socket.error, e:
    	print("Error sending data: %s" %e)
    	sys.exit(1)

    #receive response
    try:
    	print('waiting to receive')
    	data,serverREceived= sock.recvfrom(port)
    except socket.error, e:
    	print("Error sending data %s" %e)
    	sys.exit(1)
    print('received')


    if data:
    	print('close socket')
    	sock.close
    	sleep_time=random.randint(1,5)
    	print("it slept for :" + str(sleep_time)+ " seconds")
    	time.sleep(sleep_time)
    	return


# We create how many threads will be run
# The number inside range() can be altered to generate more mobile jobs using the same ID, for now it is sent at one.
#
threads = []
for i in range(5):
    t = threading.Thread(target=worker)
    threads.append(t)

    #Start the threads activity.It must be called at most once per thread object.
    t.start()                             

# We make the variable arguments which will be able to access the command line given variables we want to be able to access
# This was done just to be able to visualize the given information.
# Just done to represent info:

arguments = sys.argv

given_id = arguments[1]
given_ip = arguments[2]
given_port = arguments[3]

given_port = int(given_port)

print ("the given id was : " + str(arguments[1]))
print ("the given ip was : " + str(arguments[2]))
print ("the given port was : " + str(arguments[3]))




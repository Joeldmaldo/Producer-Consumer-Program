# Author: Joel Maldonado Rivera
# Student-ID: 801-14-3804
# H.W # 1 : Consumer and Producer problem

# We import the modules we will be using:

import socket
import threading
import random
import sys 
import time
from random import randint
from threading import Thread



"""
We define our producer function which will do the following:
 
 1) It will create a socket object and we will look for the given port argument in order to bind the object
 2) Then we will create an infinite loop which will be receiving whatever is sent to the given port.
 3) If it receives something we send that we got the job back to the mobile and used the semaphore acquire to protect our global queue
 4) After we append the work that was received into our queue we release the semaphore.
 
"""
def producer():
	"""thread worker function"""
	#must listen to messages generated by mobile devices
	# first we create the socket object
	obj = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	host = socket.gethostname() 
	system_input =sys.argv
	port = system_input[1]
	port= int(port)
	# now we will bind our object with the port we want
	obj.bind(('localhost',port))
	#pithcer #################
	#obj.listen(30)
	while True:
		#connection , address = obj.accept()     #connection established
		#print('connection was established yay')
		#connection.send('hey que la que??')
		#a=connection.recv(4017)
		#print(a)
		#connection.close()
		try:
			work , address_from = obj.recvfrom(900)   #doesn't receive fromt that port, how many bytes it will read 
		except socket.error, e:
			print( "Error receiving data: %s" %e)
			sys.exit(1)

		if work:
			got="nice job!"
			try:
				send = obj.sendto(got,address_from)
			except socket.error, e:
				print("Error sending data: %s" % e)
				sys.exit()

			# Since we are appending something to our global queue, we must use both semaphores and mutexes in order to protect it.
			print("producer acquired ")
			sema.acquire()
			Mutex.acquire()

			queue.append(work)

			Mutex.release()
			sema.release()
			print("producer released")



"""
We define our consumer function which will do the following:
 
 1) Will use the semaphore acquire to then access the queue 
 2) After doing so we use a for loop in order to split each value in the queue into mobile_id(m_id) and it's runtime.
 3) Then we release the semaphore
 4) We check if the ID already exists in our hash, if it doesn't the id will have the runtime it came with
 5) If the ID already exists the new runtime is added to the total runtime that's already in the hash.
 6) We have our global variable Nth which will allow the consumer to be able to run only a limited amount of times
 7) When Nth reaches 0 the hash information will be printed out as requested
 """

def consumer():
	#consumer must accept N numbers of element at once
	# We use sema.acquire to access queue at the given moment since its a global variable

	global Nth, queue


	while Nth!=0:

		while len(queue) == 0:
			sleep_time=random.randint(1,5)
			#print("it slept for :" + str(sleep_time)+ " seconds")
			time.sleep(sleep_time)

		sema.acquire()
		Mutex.acquire()
		print(queue)
		message=queue[0]

		Mutex.release()
		sema.release()

		split_list=message.split(':')
		m_id= split_list[0]
		runtime = split_list[1]
		runtime = int(runtime)
		if hash.has_key(m_id):
			hash[m_id] += runtime 
		else:
			hash[m_id] = runtime

		print("this is our hash: ")
		print(hash)
		
		sema.acquire()
		Mutex.acquire()
		queue.pop(0)
		Mutex.release()
		sema.release()

		# We have our Nth global value which only changes while in this thread.
		# It will limit how many mobiles the threads can handle at once,
		# If Nth reaches 0, we then print our hash with the mobile ID's and the total runtime of each
		print("THIS Nth: ")
		
		N= Nth
		N = N - 1
		Nth = N 
		print(Nth)
		if Nth==0:
			for x in hash:
				print ("Mobile "+ str(x) +" consumed " +str(hash[x]) +" of CPU seconds")

			




# We declare our global variables and semaphore

maxConnections = 10
global sema
sema = threading.BoundedSemaphore(value=maxConnections)
hash ={}
global queue
queue =[]
#Nth
Nth=10

Mutex = threading.Lock()


# We have both threads created to each execute one of the above functions.

threads = []

t = threading.Thread(target=producer)
threads.append(t)
#Start the threads activity.It must be called at most once per thread object.
t2 = threading.Thread(target=consumer)
threads.append(t2)
t.start()
t2.start()
#t.join()
#t2.join()

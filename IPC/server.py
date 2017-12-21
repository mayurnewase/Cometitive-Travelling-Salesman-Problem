#!/usr/bin/python

import _thread
from multiprocessing.connection import Listener
import threading

address = ('localhost', 6000)     # family is deduced to be 'AF_INET'
listener = Listener(address, authkey=b'secret password')

address2 = ("localhost" , 7000)
listener2 = Listener(address2 , authkey = b'password')


conn = listener.accept()
conn2 = listener2.accept()

print ('connection accepted from listener', listener.last_accepted)
print ('connection accepted from listener2', listener2.last_accepted)



def acceptFirst():
	while True:
		msg = conn.recv()
		msg = str(msg)
		print(msg)

def acceptSecond():
	while True:
		msg = conn2.recv()
		msg = str(msg)
		print(msg)
		

#_thread.start_new_thread(acceptFirst , ())
#_thread.start_new_thread(acceptSecond , ())
t1 = threading.Thread(target = acceptFirst)
t2 = threading.Thread(target = acceptSecond)

t1.daemon = True
t2.daemon = True

t1.start()
t2.start()

t1.join()
t2.join()

conn.close()
listener.close()

conn2.close()
listener2.close()

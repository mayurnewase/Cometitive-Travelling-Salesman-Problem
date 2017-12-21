from multiprocessing.connection import Client

address2 = ('localhost', 7000)
conn2 = Client(address2, authkey=b'password')

while True:
	msg = input("say something ")
	conn2.send(msg)

conn2.close()

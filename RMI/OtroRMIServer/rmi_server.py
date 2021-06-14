import Pyro5.api
import json
import threading
from socketsClass import SocketsMultibroadcast
import atexit

s = SocketsMultibroadcast()
uri = None

def sendInfoRMI():
	global uri
	toSend = {
		"rmi": True,
		"rmiCode": str(uri)
	}
	toSend = json.dumps(toSend) 
	s.sockEscritura.sendto(toSend.encode('utf-8'), (s.IP_A, s.PORT))

def receive():
	while True:
		try:
			data, address = s.sockLectura.recvfrom(1024)
			message = json.loads(data.decode('utf-8'))
			if 'getRMI' in message:
				sendInfoRMI()
			#threads.append(threading.Thread(target=sendFile))
		except Exception as e:
			print("Error!")
			print(e)
			s.closeSocketLectura()
			print("Socket de Lectura Cerrado")
			break

@Pyro5.api.expose
class Busqueda(object):
	def search(self, namefile):
		try:
			print("Busqueda: "+str(namefile))
			file = open(namefile,'r')
			return True
		except FileNotFoundError as e:
			return False
		except Exception as e:
			print ('Error: '+ str(e))
			return False

	def getFilePart(self, namefile, part, partsN):
		file = open(namefile,'rb')
		fContent = file.read()
		sizeF = len(fContent)//partsN
		print(fContent[sizeF*part:sizeF + sizeF*part])
		return fContent[sizeF*part:sizeF + sizeF*part]

def rmi():
	global uri
	daemon = Pyro5.api.Daemon()             # make a Pyro daemon
	uri = daemon.register(Busqueda,"busqueda")
	#ns.register("example.greeting", uri)  # register name
	print("Ready. Object uri =", uri)       # print the uri so we can use it in the client later
	sendInfoRMI()
	daemon.requestLoop()                    # start the event loop of the server to wait for calls

def closeServer():
	toSend = {
		"close": True,
		"rmiCode": str(uri)
	}
	toSend = json.dumps(toSend) 
	s.sockEscritura.sendto(toSend.encode('utf-8'), (s.IP_A, s.PORT))
	s.closeSockets()

if __name__ == "__main__":
	atexit.register(closeServer)
	threads = []
	threads.append(threading.Thread(target=rmi))
	threads.append(threading.Thread(target=receive))
	[t.start() for t in threads]
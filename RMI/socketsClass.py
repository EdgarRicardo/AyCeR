import socket
import struct
import sys

class SocketsMultibroadcast():
	"""docstring for ClassName"""
	IP_A = '224.0.0.1'
	PORT = 12345
	def __init__(self):
		self.createSocketEscritura()
		self.createSocketLectura()

	def createSocketEscritura(self):
		self.sockEscritura = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		# self.sockEscritura.settimeout(0.2)
		ttl = struct.pack('b', 1)
		self.sockEscritura.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

	def createSocketLectura(self):
		multicast_group = self.IP_A
		server_address = ('', self.PORT)
		self.sockLectura  = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		# Tell the operating system to add the socket to
		# the multicast group on all interfaces.
		group = socket.inet_aton(multicast_group)
		mreq = struct.pack('4sL', group, socket.INADDR_ANY)
		self.sockLectura .setsockopt(socket.IPPROTO_IP,socket.IP_ADD_MEMBERSHIP, mreq)
		self.sockLectura .setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		# Bind to the server address
		self.sockLectura .bind(server_address)

	def closeSocketEscritura(self):
		self.sockEscritura.close()

	def closeSocketLectura(self):
		self.sockLectura.close()
	
	def closeSockets(self):
		self.closeSocketEscritura()
		self.closeSocketLectura()

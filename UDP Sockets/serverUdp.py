import socket
import sys
import json
import os

def serverSocket():
	# Create a UDP socket
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

	# Bind the socket to the port
	server_address = ('localhost', 12345)
	print('Servidor iniciado en {} puerto {}'.format(*server_address))
	sock.bind(server_address)

	while True:
		print('\nEsperando mensaje')
		data, address = sock.recvfrom(4096)

		if data:
			res = json.loads(data.decode('utf-8'))
			print(res)
			mensaje = res["mensaje"]

			print('Mensaje de {} bytes desde {}'.format(res["size"], address))
			
			sent = sock.sendto(str.encode(mensaje), address)
			print('Enviando acuse del segmento '+ str(res["segmento"]) +' del mensaje '+ mensaje +' a {}'.format(address))

if __name__ == "__main__":
	serverSocket()

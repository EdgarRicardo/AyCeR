import socket
import sys
import json
import os

BUFFER_SIZE = 10

def clientSocket():
	try:
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		server_address = ('localhost', 12345)

		print("Para salir escribe 'salir'")
		mensaje = input("Ingresa un mensaje para el server: ")
		while(mensaje != 'salir'):
			for i in range(0,len(mensaje)//BUFFER_SIZE+1):
				segmento = mensaje[i*BUFFER_SIZE:(i*BUFFER_SIZE)+BUFFER_SIZE]
				data = {
					"segmento": i,
					"size": len(segmento),
					"mensaje": segmento
				}
				print(data)
				toSend = json.dumps(data)
				# Send data
				print('\nEnviando segmento '+str(i)+': '+ segmento)
				sent = sock.sendto(toSend.encode('utf-8'), server_address)

				# Receive response
				print('Esperando acuse')
				data, server = sock.recvfrom(BUFFER_SIZE)
				print('Recibido {!r}'.format(data))

			mensaje = input("Ingresa un mensaje para el server: ")

	finally:
		print('Cerrando socket')
		sock.close()

if __name__ == "__main__":
    clientSocket()

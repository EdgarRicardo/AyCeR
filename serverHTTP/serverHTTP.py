import socket
from concurrent.futures import ThreadPoolExecutor
import mimetypes

# Define socket host and port
SERVER_HOST = 'localhost'
SERVER_PORT = 8001
PUBLIC = 'public'

def get(client,headers):
	filename = headers[0].split()[1]
	# Get the content of the file
	if filename == '/':
		filename = '/index.html'

	try:
		# Send HTTP response
		file = open(PUBLIC+filename,'rb')
		fContent = file.read()
		file.close()
		mimeType = mimetypes.guess_type(PUBLIC+filename)
		response = 'HTTP/1.1 200 OK\n'
		response += 'Content-Type:'+mimeType[0]+'\n'
		response += 'Content-Length:'+str(len(fContent))+'\n\n\r'
		response = response.encode('utf-8')
		response += fContent
		client.send(response)
		client.close()
	except FileNotFoundError:
		response = b'HTTP/1.1 404 NOT FOUND\n\n\rFile Not Found'
		client.send(response)
		client.close()
	except Exception as e:
		print(e)
		client.close()

def post(client,headers):
	filename = headers[0].split()[1]
	# Get the content of the file
	if filename == '/':
		filename = '/post.html'

	try:
		# Send HTTP response
		file = open(PUBLIC+filename,'rb')
		fContent = file.read()
		file.close()
		mimeType = mimetypes.guess_type(PUBLIC+filename)
		response = 'HTTP/1.1 200 OK\n'
		response += 'Content-Type:'+mimeType[0]+'\n'
		response += 'Content-Length:'+str(len(fContent))+'\n\n\r'
		response = response.encode('utf-8')
		response += fContent
		client.send(response)
		client.close()
	except FileNotFoundError:
		response = b'HTTP/1.1 404 NOT FOUND\n\n\rFile Not Found'
		client.send(response)
		client.close()
	except Exception as e:
		print(e)
		client.close()

def put(client,headers):
	filename = headers[0].split()[1]
	# Get the content of the file
	if filename == '/':
		filename = '/put.html'

	try:
		# Send HTTP response
		file = open(PUBLIC+filename,'rb')
		fContent = file.read()
		file.close()
		mimeType = mimetypes.guess_type(PUBLIC+filename)
		response = 'HTTP/1.1 200 OK\n'
		response += 'Content-Type:'+mimeType[0]+'\n'
		response += 'Content-Length:'+str(len(fContent))+'\n\n\r'
		response = response.encode('utf-8')
		response += fContent
		client.send(response)
		client.close()
	except FileNotFoundError:
		response = b'HTTP/1.1 404 NOT FOUND\n\n\rFile Not Found'
		client.send(response)
		client.close()
	except Exception as e:
		print(e)
		client.close()

def head(client,headers):
	filename = headers[0].split()[1]
	# Get the content of the file
	if filename == '/':
		filename = '/index.html'

	try:
		# Send HTTP response
		file = open(PUBLIC+filename,'rb')
		fContent = file.read()
		file.close()
		mimeType = mimetypes.guess_type(PUBLIC+filename)
		response = 'HTTP/1.1 200 OK\n'
		response += 'Content-Type:'+mimeType[0]+'\n'
		response += 'Content-Length:'+str(len(fContent))
		response = response.encode('utf-8')
		client.send(response)
		client.close()
	except FileNotFoundError:
		response = b'HTTP/1.1 404 NOT FOUND'
		client.send(response)
		client.close()
	except Exception as e:
		print(e)
		client.close()

def threadClient(client,addr):
	with client:
		# Client request
		request = client.recv(1024).decode()

		# Parse HTTP headers
		headers = request.split('\n')
		typeRequest = headers[0].split()[0]

		if typeRequest == "GET":
			get(client,headers)
		elif typeRequest == "POST":
			post(client,headers)
		elif typeRequest == "PUT":
			put(client,headers)
		elif typeRequest == "HEAD":
			head(client,headers)
		else:
			response = b'HTTP/1.1 405 METHOD NOT ALLOWED\n\n\rMetodo no permitido'
			client.send(response)
			client.close()


		

if __name__ == "__main__":

	# Pool de Hilos
	pool = ThreadPoolExecutor(max_workers=10)

	# Crear socket
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_tcp:
		socket_tcp.bind((SERVER_HOST, SERVER_PORT)) 
		socket_tcp.listen(5)
		print('Abriendo servidor HTTP en %s ...' % SERVER_PORT)

		while True:    
		    #Conexiones
		    client, addr = socket_tcp.accept()
		    print(addr)
		    pool.submit(threadClient, client, addr)
	    

	# Close socket
	server_socket.close()

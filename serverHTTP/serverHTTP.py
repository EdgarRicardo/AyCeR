import socket
from concurrent.futures import ThreadPoolExecutor
import mimetypes
from pprint import pprint

# Define socket host and port
SERVER_HOST = 'localhost'
SERVER_PORT = 8001
PUBLIC = 'public'

def get(headers):
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
		response = 'HTTP/1.1 200 OK\r\n'
		response += 'Content-Type:'+mimeType[0]+'\r\n'
		response += 'Content-Length:'+str(len(fContent))+'\r\n'
		response += 'Accept-Ranges: bytes\r\n\n'
		response = response.encode('utf-8')
		response += fContent
		return response
	except FileNotFoundError:
		response = 'HTTP/1.1 404 NOT FOUND\r\n\nArchivo no encontrado'
		return response.encode('utf-8')
	except Exception as e:
		response = 'HTTP/1.1 500  INTERNAL SERVER ERROR\r\n\nError en el servidor: '+str(e)
		return response.encode('utf-8')



def post(headers):
	pprint(headers)
	filename = headers[0].split()[1]
	# Get the content of the file
	if filename == '/':
		filename = '/post.html'
	try:
		# Send HTTP response
		mimeType = mimetypes.guess_type(PUBLIC+filename)
		file = open(PUBLIC+filename,'rb')
		fContent = file.read()
		file.close()
		response = 'HTTP/1.1 200 OK\r\n'
		response += 'Content-Type:'+mimeType[0]+'\r\n'
		response += 'Content-Length:'+str(len(fContent))+'\r\n\n'
		response = response.encode('utf-8')
		response += fContent
		return response
	except FileNotFoundError as e:
		return b'HTTP/1.1 404 NOT FOUND\r\n\nArchivo no encontrado';
	except Exception as e:
		response = 'HTTP/1.1 500  INTERNAL SERVER ERROR\r\n\nError en el servidor: '+str(e)
		return response.encode('utf-8')

def put(request):
	print(request.split(b'\r\n'))
	# filename = headers[0].split()[1]
	# Get the content of the file
	filename = '/'
	if filename == '/':
		filename = '/put.html'
	try:
		# Send HTTP response
		file = open(PUBLIC+filename,'rb')
		fContent = file.read()
		file.close()
		mimeType = mimetypes.guess_type(PUBLIC+filename)
		response = 'HTTP/1.1 200 OK\n'
		response += 'Content-Type:'+mimeType[0]+'\r\n'
		response += 'Content-Length:'+str(len(fContent))+'\r\n\n'
		response = response.encode('utf-8')
		response += fContent
		return response
	except FileNotFoundError as e:
		return b'HTTP/1.1 404 NOT FOUND\r\n\nArchivo no encontrado';
	except Exception as e:
		response = 'HTTP/1.1 500  INTERNAL SERVER ERROR\r\n\nError en el servidor: '+str(e)
		return response.encode('utf-8')

def head(headers):
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
		response = 'HTTP/1.1 200 OK\r\n'
		response += 'Content-Type:'+mimeType[0]+'\r\n'
		response += 'Content-Length:'+str(len(fContent))+'\r\n\n'
		response = response.encode('utf-8')
		return response
	except FileNotFoundError as e:
		return b'HTTP/1.1 404 NOT FOUND\r\n\n';
	except Exception as e:
		response = 'HTTP/1.1 500  INTERNAL SERVER ERROR\r\n\nError en el servidor: '+str(e)
		return response.encode('utf-8')

def threadClient(client,addr):
	try:
		data = client.recv(65535)
		request = data
		while data:
			try:
				client.settimeout(0.01)
				data = client.recv(65535)
				client.settimeout(None)
			except Exception:
				break;
			request += data
		# Parse HTTP headers
		typeRequest = request[:20].decode('utf-8').split('\r\n')[0].split()[0]

		if typeRequest != "PUT":
			request = request.decode('utf-8')
			headers = request.split('\r\n')

		if typeRequest == "GET":
			response = get(headers)
		elif typeRequest == "POST":
			response = post(headers)
		elif typeRequest == "PUT":
			response = put(request)
		elif typeRequest == "HEAD":
			response = head(headers)
		else:
			response = b'HTTP/1.1 405 METHOD NOT ALLOWED\r\n\nMetodo no permitido'

		client.send(response)		
		client.close()
	except Exception as e:
		response = 'HTTP/1.1 500  INTERNAL SERVER ERROR\r\n\nError en el servidor: '+str(e)
		response = response.encode('utf-8')
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

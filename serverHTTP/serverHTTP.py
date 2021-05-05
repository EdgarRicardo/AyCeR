import socket
from concurrent.futures import ThreadPoolExecutor
import mimetypes
from pprint import pprint

# Define socket host and port
SERVER_HOST = 'localhost'
SERVER_PORT = 8001
PUBLIC = 'public'

def get(request):
	filename = request[0].decode('utf-8').split()[1]
	# Get the content of the file
	if filename == '/':
		filename = '/index.html'
	else:
		filename = '/getFiles/'+filename
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



def post(request):
	for x in request:
		print(x)
	filename = request[0].decode('utf-8').split()[1]
	# Get the content of the file
	if 'getFiles' in filename:
		return b'HTTP/1.1 405 METHOD NOT ALLOWED\r\n\nMetodo no permitido para este archivo'
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
		return b'HTTP/1.1 404 NOT FOUND\r\n\nArchivo no encontrado'
	except Exception as e:
		response = 'HTTP/1.1 500  INTERNAL SERVER ERROR\r\n\nError en el servidor: '+str(e)
		return response.encode('utf-8')

def put(request):
	boundary = None
	for x in request:
		if b'boundary' in x:
			boundary = x
		print(x)
	print(boundary)
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

def head(request):
	filename = request[0].decode('utf-8').split()[1]
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
		arrayRequest = request.split(b'\r\n')
		typeRequest = arrayRequest[0].decode('utf-8').split()[0]

		if typeRequest == "GET":
			response = get(arrayRequest)
		elif typeRequest == "POST":
			response = post(arrayRequest)
		elif typeRequest == "PUT":
			response = put(arrayRequest)
		elif typeRequest == "HEAD":
			response = head(arrayRequest)
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

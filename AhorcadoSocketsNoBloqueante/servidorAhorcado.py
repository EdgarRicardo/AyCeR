import socket
import random
import json
import sys
import selectors
import socket

selector = selectors.DefaultSelector()
host = socket.gethostname() # Esta función nos da el nombre de la máquina
port = 12345
BUFFER_SIZE = 1024

facil = [
    "casa",
    "perro",
    "gato",
    "pera"
]
intermedio = [
    "montaña",
    "laguna",
    "manzana",
    "computadora"

]
dificil = [
    "la casa verde",
    "esto es dificil",
    "redes de computadoras"
]

def is_json(jsonVerify):
  try:
    load = json.loads(jsonVerify)
  except ValueError as e:
    return False
  return load

def closeClient(conn,addr):
    try:
        conn.close()
        selector.unregister(conn)
        print("Se desconecto el client: "+str(addr))
    except Exception as e:
        print("Se desconecto el client: "+str(addr))
        print("Error: "+str(e))

def read(conn,mask):
    addr = conn.getpeername()
    try:
        data = conn.recv(BUFFER_SIZE)
        if data:
            if type(is_json(data.decode('utf-8'))) is int:
                dif = data.decode('utf-8')
                print('[*] Dificultad elegida por '+str(addr)+' : ' + dif)
                palabra = ""
                if int(dif) == 1:
                    palabra = random.choice(facil)
                elif int(dif) == 2:
                    palabra = random.choice(intermedio)
                elif int(dif) == 3:
                    palabra = random.choice(dificil)
                conn.send(str(palabra).encode('utf-8'))
            elif is_json(data.decode('utf-8')):
                scoresFile = open('scores.txt','a+')
                toSave = json.loads(data.decode('utf-8'))
                if toSave["win"]:
                    win = "Ganador"
                else:
                    win = "Perdedor"
                print(win+" "+toSave["nickname"]+": "+str(addr))
                scoresFile.write('\n'+str(addr)+" "+win+": "+toSave["nickname"]+' en '+str(toSave["time"])+' seg en dificultad '+str(toSave["dif"])+'\n')
                scoresFile.close()
                closeClient(conn,addr)
    except socket.error as e:
        closeClient(conn,addr)
        print("Error: "+str(e))
    except Exception as e:
        print("Se desconecto el client: "+str(addr))
        print("Error: "+str(e))
    

def accept(socket_tcp,mask):
    conn, addr = socket_tcp.accept() # Establecemos la conexión con el cliente
    conn.setblocking(False)
    print('[*] Conexión establecida con: ', addr)  
    selector.register(conn, selectors.EVENT_READ, read)

def socketServidor():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_tcp: #socket.AF_INE -> IPv4 ; socket.SOCK_STREAM -> TCP : Socket TCP/IP
        socket_tcp.bind((host, port)) 
        socket_tcp.listen(5) # Esperamos la conexión del cliente y capacidad de la cola de conexiones pendientes
        socket_tcp.setblocking(False)
        selector.register(socket_tcp, selectors.EVENT_READ, accept)
        while True:
            print('Esperando usuario') 
            for key, mask in selector.select(timeout=1):
                callback = key.data
                callback(key.fileobj, mask)
                

if __name__ == "__main__":
    socketServidor()

    

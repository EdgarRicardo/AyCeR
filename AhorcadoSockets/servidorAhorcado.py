import socket
import random
import json
import sys

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


def socketServidor():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_tcp: #socket.AF_INE -> IPv4 ; socket.SOCK_STREAM -> TCP : Socket TCP/IP
        socket_tcp.bind((host, port)) 
        socket_tcp.listen(5) # Esperamos la conexión del cliente y capacidad de la cola de conexiones pendientes
        while True:
            print('waiting for a connection') 
            conn, addr = socket_tcp.accept() # Establecemos la conexión con el cliente
            try:
                with conn:
                    print('[*] Conexión establecida con: ', addr)  
                    # Verificamos que hemos recibido datos
                    while True:
                        data = conn.recv(BUFFER_SIZE)
                        if data:
                            dif = data.decode('utf-8')
                            print('[*] Dificultad elegida: ' + dif)
                            palabra = ""
                            if int(dif) == 1:
                                palabra = random.choice(facil)
                            elif int(dif) == 2:
                                palabra = random.choice(intermedio)
                            elif int(dif) == 3:
                                palabra = random.choice(dificil)

                            conn.send(str(palabra).encode('utf-8'))
                            data = conn.recv(BUFFER_SIZE)
                            if data:
                                scoresFile = open('scores.txt','a+')
                                toSave = json.loads(data.decode('utf-8'))
                                scoresFile.write('\n'+toSave["nickname"]+': '+str(toSave["time"])+' seg en dificultad '+dif+'\n')
                                scoresFile.close()
                        else:
                            break
            finally:
                # Clean up the connection
                conn.close()
    

if __name__ == "__main__":
    socketServidor()

    

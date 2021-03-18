import socket
import random
import json
import sys

host = socket.gethostname() # Esta función nos da el nombre de la máquina
port = 12345
BUFFER_SIZE = 1024

animales = ["leon","perro","gato","lagartija","serpiente","caballo","tiburon","cucaracha","ardilla","tigre","conejo","abeja","burro","cerdo","jirafa","tortuga"]
cocina = ["tenedor","plato","cuchara","sarten","cuchillo","sopa","estufa","refrigerador","comida","cacerola","cubiertos","especia","sal","ajo","horno","microondas","embudo"]
oficina = ["archivo","computadora","lapiz","plumas","hojas","jefe","papelera","tijeras","agenda","engrapadora","impresora","calendario","contabilidad","finanzas","escritorio","telefono"]
frutas = ["naranja","pera","melon","sandia","fresa","guayaba","manzana","papaya","mango","piña","platano","uvas","arandano","mandarina","cereza","zarzamora"]

def generarSopa(categoria):
    print("Test")

def socketServidor():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_tcp: #socket.AF_INE -> IPv4 ; socket.SOCK_STREAM -> TCP : Socket TCP/IP
        socket_tcp.bind((host, port)) 
        socket_tcp.listen(5) # Esperamos la conexión del cliente y capacidad de la cola de conexiones pendientes
        while True:
            print('Esperando conexion') 
            conn, addr = socket_tcp.accept() # Establecemos la conexión con el cliente
            try:
                with conn:
                    print('[*] Conexión establecida con: ', addr)  
                    # Verificamos que hemos recibido datos
                    while True:
                        data = conn.recv(BUFFER_SIZE)
                        if data:
                            dif = data.decode('utf-8')
                            print('[*] Categoria elegida: ' + dif)
                            palabra = ""
                            if int(dif) == 1:
                                generarSopa(animales)
                            elif int(dif) == 2:
                                generarSopa(cocina)
                            elif int(dif) == 3:
                                generarSopa(oficina)
                            elif int(dif) == 4:
                                generarSopa(frutas)

                            #Se enviara la sopa de letras + el array con las palabras a encomtar
                            #conn.send()

                            data = conn.recv(BUFFER_SIZE)
                            if data:
                                scoresFile = open('scores.txt','a+')
                                toSave = json.loads(data.decode('utf-8'))
                                scoresFile.write('\n'+toSave["nickname"]+': '+str(toSave["time"])+' seg en la categoria '+dif+'\n')
                                scoresFile.close()
                            else:
                                break
                        else:
                            break
            finally:
                # Clean up the connection
                conn.close()
    

if __name__ == "__main__":
    socketServidor()

    

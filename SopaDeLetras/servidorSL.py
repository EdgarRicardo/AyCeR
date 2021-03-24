import socket
import random
import json
import sys
from generarSopa import Sopa
import pprint

host = socket.gethostname() # Esta función nos da el nombre de la máquina
port = 12346
BUFFER_SIZE = 65000
size = 15
sopaClass = Sopa()

animales = ["leon","perro","gato","lagartija","serpiente","caballo","tiburon","cucaracha","ardilla","tigre","conejo","abeja","burro","cerdo","jirafa","tortuga","hormiga","elefante","pato","peces"]
cocina = ["tenedor","plato","cuchara","sarten","cuchillo","sopa","estufa","refrigerador","comida","cacerola","cubiertos","especia","sal","ajo","horno","microondas","embudo","receta","cocinero","chef","pinche"]
oficina = ["archivo","computadora","lapiz","plumas","hojas","jefe","papelera","tijeras","agenda","engrapadora","impresora","calendario","contabilidad","finanzas","escritorio","telefono","godinez","quincena","reportes","dinero"]
frutas = ["naranja","pera","melon","sandia","fresa","guayaba","manzana","papaya","mango","piña","platano","uvas","arandano","mandarina","cereza","zarzamora","frambuesa","limon","coco","higo"]
pruebas = ["casa","perro","computadora","lagartija"]

def generarSopa(categoria):
    sopa = [["" for y in range(size+1)] for x in range(size+1)]
    datosPalabras = {}
    
    for el in categoria:
        sopaClass.posicionarPalabra(el,sopa,datosPalabras)

    for x in range(size+1): 
        for y in range(size+1):
            if sopa[x][y]  == "":
                sopa[x][y] =  random.choice('abcdefghijklmnñopqrstuvwxyz')

    sopaClass.printSopa(sopa)
    pprint.pprint(datosPalabras)

    return sopa, datosPalabras

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
                            if int(dif) == 1:
                                sopa,datosPalabras = generarSopa(animales)
                            elif int(dif) == 2:
                                sopa,datosPalabras = generarSopa(cocina)
                            elif int(dif) == 3:
                                sopa,datosPalabras = generarSopa(oficina)
                            elif int(dif) == 4:
                                sopa,datosPalabras = generarSopa(frutas)
                            elif int(dif) == 5:
                                sopa,datosPalabras = generarSopa(pruebas)

                            sopaLetras = {
                                "sopa": sopa,
                                "datosPalabras": datosPalabras 
                            }

                            #Se enviara la sopa de letras + el array con las palabras a encontrar
                            res = json.dumps(sopaLetras)
                            conn.send(res.encode('utf-8'))
                            
                            #Esperamos que el cliente nos envie el score
                            print("Esperando score del usuario")
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
                print('Se cerró la conexión con', addr)
                conn.close()
    

if __name__ == "__main__":
    socketServidor()

    

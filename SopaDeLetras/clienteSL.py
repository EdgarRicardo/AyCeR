import socket
from datetime import datetime
import json
import pprint
from generarSopa import Sopa
import os

sopaClass = Sopa()
host = socket.gethostname()
port = 12346
BUFFER_SIZE = 65000

def borrarPantalla(): # Borrar pantalla para cualquier sistema
    if os.name == "posix":
       os.system ("clear")
    elif os.name == "ce" or os.name == "nt" or os.name == "dos":
       os.system ("cls")

def socketCliente():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_tcp:
        socket_tcp.connect((host, port))
        try:
            print("1.- Animales")
            print("2.- Cocina")
            print("3.- Oifcina")
            print("4.- Frutas")
            print("Selecione una categoria: ")
            dificultad = input()
            if dificultad in ["1","2","3","4"]:
                socket_tcp.send(str(dificultad).encode('utf-8'))

                # Se recibiran la sopa de letras y el array de palabras con sus coordenadas
                data = socket_tcp.recv(BUFFER_SIZE)
                sopaLetras = json.loads(data.decode('utf-8'))

                sopa = sopaLetras["sopa"] # Es la sopa de letras como tal
                datosPalabras = sopaLetras["datosPalabras"] # Los datos por palabras de su inicio y fin 

                
                input("Se obtuvo la sopa con las palabras que eligio, desde el momento que se muestre la sopa \n su tiempo comenzara a correr. Suerte!!!...")
               
                tiempo = operacionesJugador(sopa,datosPalabras)
                #Juego

                print("Felicidades crack, acabaste en " + str(tiempo) + "seg!!!\nDanos un nickname para registrar tu score: ")
                nickname = input()
                data = {
                    "time": tiempo,
                    "nickname": nickname
                }
                res = json.dumps(data) 
                socket_tcp.send(res.encode('utf-8'))
            else:
                print("Dificultad no valida :(")
        finally:
            print('closing socket')
            socket_tcp.close()

def operacionesJugador(sopa,palabras):
    borrarPantalla()
    bandera = True
    palabrasFaltantes = list(palabras.values())

    startTime = datetime.now()
    while bandera:
        borrarPantalla()
        print("Ingrese las coordenadas de la palabra que encontró: ")
        print()
        sopaClass.printSopa(sopa)
        print()
        print("Palabras que te hacen falta:",end=" ")
        print(palabrasFaltantes)
        coordenadasElegida = input("Ingresa las coordenadas de la palabra que encontraste con el siguiente\nformato FilaInicio,ColumnaInicial,FilaFinal,ColumnaFinal: ")
        resultado = palabras.get(coordenadasElegida)

        if  resultado == None:
            input("Error, esas coordenadas no corresponden con ninguna de las palabras...")
        else:
            input("Muy bien, encontraste la palabra "+resultado)
            palabrasFaltantes.remove(resultado)
            if len(palabrasFaltantes) == 0:
                endTime = datetime.now()
                bandera = False

    
    time = (endTime - startTime)
    return time.total_seconds()
        
if __name__ == "__main__":
    socketCliente()


    

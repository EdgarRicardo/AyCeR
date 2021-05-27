import socket
from datetime import datetime
import json

host = socket.gethostname()
port = 12345
BUFFER_SIZE = 1024

def socketCliente():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_tcp:
        socket_tcp.connect((host, port))
        try:
            print("1.- Facil")
            print("2.- Intermedio")
            print("3.- Dificil")
            print("Selecione una dificultad: ")
            dificultad = input()
            # Convertimos str a bytes
            if dificultad in ["1","2","3"]:
                socket_tcp.send(str(dificultad).encode('utf-8'))
                data = socket_tcp.recv(BUFFER_SIZE)
                palabra = data.decode('utf-8')
                tamanio = len(palabra)
                if tamanio > 0:
                    nintentos = 8
                    win = False
                    startTime = datetime.now()
                    palabraOculta = palabraOcultaStart(palabra)
                    while nintentos > 0:
                        print(palabraOculta , "\nIntentos restantes: " + str(nintentos))
                        if(verifyWin(palabraOculta)):
                            win = True
                            break
                        print("Prueba suerte: ")
                        intento = input()
                        if len(intento) == 1:
                            palabraOculta, existio = getPalabraOculta(palabraOculta, palabra, intento)
                            if not existio:
                                nintentos = nintentos - 1
                        else:
                            print("No te quieras pasar de listo! jeje")
                            nintentos = nintentos - 1

                    endTime = datetime.now()
                    time = (endTime - startTime)
                    realTime = time.total_seconds()

                    data = {
                            "time": realTime,
                            "nickname": "",
                            "dif": dificultad,
                            "win": True
                    }
                    if(win):
                        print("Felicidades crack, ganaste!!!\nDanos un nickname para registrar tu score de: "+str(realTime)+" seg")
                        data["win"] = True
                    else:
                        print("Suerte para la próxima, fracasado!!! jajaja\nDanos un nickname para registrar tu miserable fracaso")
                        data["win"] = False
                    
                    nickname = input()
                    data["nickname"] = nickname
                    res = json.dumps(data) 
                    socket_tcp.send(res.encode('utf-8'))

                else:
                    print("Problemas en el server jeje :(")
            else:
                print("Dificultad no valida :(")
        finally:
            print('closing socket')
            socket_tcp.close()

def palabraOcultaStart(palabra):
    palabraOculta = ""
    for p in palabra:
        palabraOculta += "*"
    return palabraOculta

def verifyWin(palabraOculta):
    return "*" not in palabraOculta

def getPalabraOculta(palabraOculta,palabra,intento):
    oculta = ""
    for idx, p in enumerate(palabra):
        if palabraOculta[idx] != "*":
            oculta += palabraOculta[idx]
        elif p == intento:
            oculta += p
        else:
            oculta+= "*"
    return oculta, intento.lower() in palabra.lower()

if __name__ == "__main__":
    socketCliente()


    

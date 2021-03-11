import socket
from datetime import datetime
import json
from tkinter import filedialog
from tkinter import *
import shutil
import os
from zipfile import ZipFile

host = socket.gethostname()
port = 12345
BUFFER_SIZE = 1024

def pedirNumeroEntero():
    num = 0
    while (num < 1 or num > 8):
        try:
            num = int(input("Introduce la opción: "))
        except:
            print('Error, introduce una opcion valida')
    return num

def menuOpts():
    print("Drive con sockets: Los archivos y carpetas seran creados en el directorio actual")
    print("1.- Ver directorios/archivos del directorio actual")
    print("2.- Cambiar de directorio")
    print("3.- Subir archivo al drive")
    print("4.- Subir carpeta al drive")
    print("5.- Eliminar archivo del drive")
    print("6.- Eliminar carpeta del drive")
    print("7.- Nueva carpeta del drive")
    print("8.- Salir")
    return pedirNumeroEntero()

def borrarPantalla():
    if os.name == "posix":
       os.system ("clear")
    elif os.name == "ce" or os.name == "nt" or os.name == "dos":
       os.system ("cls")

def socketCliente():
    data = {
        "opcion": 0,
        "directorio": "",
        "binary": ""  
    }
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_tcp:
        socket_tcp.connect((host, port))
        try:
            path = ""
            while True:
                borrarPantalla()
                print("Current Path", path)
                opt = menuOpts()
                if opt in [1,5,6]:
                    sendInfo(socket_tcp,{"opt":opt,"path":path})
                    res = readRes(socket_tcp)
                    if opt == 1:
                        print("Directorios: ", res["directorios"])
                        print("Archivos: ", res["archivos"])
                    elif opt in [5,6]:
                        if opt == 5:
                            print("Archivos validos: ", res["archivos"])
                            name = input("Ingresa el nombre del archivo: ")
                        else:
                            print("Directorios validos: ", res["directorios"])
                            name = input("Ingresa el nombre del directorio: ")

                        if (opt == 5 and name in res["archivos"]) or (opt == 6 and name in res["directorios"]):
                            data = {
                                "path": path,
                                "name": name
                            }
                            sendInfo(socket_tcp,data)
                            msg = readRes(socket_tcp)["message"]
                            print(msg)
                        else:
                            sendInfo(socket_tcp,{"error":1})
                            print("Nombre no valido")

                    input("Press Enter to continue...")
                elif opt == 2:
                    sendInfo(socket_tcp,{"opt":opt,"path":path})
                    res = readRes(socket_tcp)
                    if path != "":
                        res["directorios"].append("..")
                    print("Directorios validos: ", res["directorios"])
                    directorio = input("Ingrese el nombre del directorio: ")
                    if directorio in res["directorios"]:
                        if directorio == "..":
                            auxPath = path.split("/")
                            auxPath.pop(-1)
                            separator = '/'
                            path = separator.join(auxPath)
                        else:
                            path += "/"+directorio
                    else:
                        print("Directiro no valido")
                    input("Press Enter to continue...")
                elif opt == 3:
                    fileName, file, fileSize = readFile()
                    if fileName:
                        data = {
                            "opt": opt,
                            "fileName": fileName,
                            "path": path,
                            "fileSize": fileSize
                        }

                        sendInfo(socket_tcp, data)
                        for i in range(0,fileSize//BUFFER_SIZE+1):
                            content = file.read(BUFFER_SIZE)
                            socket_tcp.sendall(content)
                        
                        file.close()
                        msg = readRes(socket_tcp)["message"]
                        print(msg)
                    input("Press Enter to continue...")
                elif opt == 4:
                    fileName, directory = readDirectory()
                    if fileName:
                        archivo_zip = shutil.make_archive("carpetaToSend","zip",directory)
                        file_stats = os.stat(archivo_zip)
                        fileSize = file_stats.st_size
                        data = {
                            "opt": opt,
                            "fileName": fileName,
                            "path": path,
                            "fileSize": fileSize
                        }

                        file = open(archivo_zip,"rb")
                        sendInfo(socket_tcp, data)
                        for i in range(0,fileSize//BUFFER_SIZE+1):
                            content = file.read(BUFFER_SIZE)
                            socket_tcp.sendall(content)
                        
                        print("Salí")
                        file.close()
                        os.remove(archivo_zip)
                        msg = readRes(socket_tcp)["message"]
                        print(msg)
                    input("Press Enter to continue...")
                elif opt == 7:
                    directoryName = input("Ingresa el nombre del directorio: ")
                    data = {
                        "opt": opt,
                        "directoryName": directoryName,
                        "path": path
                    }
                    sendInfo(socket_tcp, data)
                    msg = readRes(socket_tcp)["message"]
                    print(msg)
                    input("Press Enter to continue...")
                else:
                    break 
        finally:
            print('Conexión Cerrada')
            socket_tcp.close()

def readDirectory():
    try:
        root = Tk()
        root.withdraw() # Quitar ventana de tkinter
        directory = filedialog.askdirectory(initialdir = ".",title = "Selelecciona la carpeta")
        fileName = directory.split("/")[-1]
        return fileName, directory
    except Exception as e:
        print(e)
        return None, None

def readFile():
    try:
        root = Tk()
        root.withdraw() # Quitar ventana de tkinter
        file =  filedialog.askopenfile(mode="rb",initialdir = ".",title = "Selelecciona tu archivo")
        file_stats = os.stat(file.name)
        fileName = os.path.basename(file.name)
        return fileName, file, file_stats.st_size
    except Exception as e:
        print(e)
        return None, None, None

def sendInfo(socket_tcp, data):
    toSend = json.dumps(data) 
    socket_tcp.send(toSend.encode('utf-8'))

def readRes(socket_tcp):
    res = socket_tcp.recv(BUFFER_SIZE)
    data = json.loads(res.decode('utf-8'))
    return data

if __name__ == "__main__":
    socketCliente()

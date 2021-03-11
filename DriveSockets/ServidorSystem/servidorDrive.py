import socket
import random
import json
import shutil
import os

host = socket.gethostname() # Esta función nos da el nombre de la máquina
port = 12345
BUFFER_SIZE = 1024

def sendInfo(conn, data):
    toSend = json.dumps(data) 
    conn.send(toSend.encode('utf-8'))

def getFiles(path):
    res = {}
    for (dirpath, dirnames, filenames) in os.walk(path):
        res["directorios"] = dirnames
        res["archivos"] = filenames
        break
    return res    

def socketServidor():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_tcp: #socket.AF_INE -> IPv4 ; socket.SOCK_STREAM -> TCP : Socket TCP/IP
        socket_tcp.bind((host, port)) 
        socket_tcp.listen(5) # Esperamos la conexión del cliente y capacidad de la cola de conexiones pendientes
        while True:
            print('Esperando conexión') 
            conn, addr = socket_tcp.accept() # Establecemos la conexión con el cliente
            #os.chdir("./Drive") #Nos movemos a la carpeta que simula el drive
            initialPath = "./Drive"
            try:
                with conn:
                    print('[*] Conexión establecida con: ', addr)
                    while True:
                        data = conn.recv(BUFFER_SIZE)
                        if data:
                            res = json.loads(data.decode('utf-8'))
                            if res["opt"] in [1,2,5,6]:
                                path = initialPath+res["path"]
                                files = getFiles(path)
                                sendInfo(conn,files)
                                if res["opt"] in [5,6]:
                                    data = conn.recv(BUFFER_SIZE)
                                    if data:
                                        res2 = json.loads(data.decode('utf-8'))
                                        if "error" not in res2:
                                            path = initialPath+res2["path"]+"/"+res2["name"]
                                            if res["opt"] == 5:
                                                os.remove(path)
                                                sendInfo(conn,{"message":"Archivo eliminado correctamente"})
                                            else:
                                                shutil.rmtree(path)
                                                sendInfo(conn,{"message":"Carpeta eliminada correctamente"})                    
                            elif res["opt"] == 3:
                                try:
                                    path = initialPath+res["path"]+"/"+res["fileName"]
                                    fileSize = res["fileSize"]
                                    file = open(path,"wb")

                                    for i in range(0,fileSize//BUFFER_SIZE+1):
                                        content = conn.recv(BUFFER_SIZE)
                                        file.write(content)

                                    print('Salí')
                                    file.close()
                                    sendInfo(conn,{"message":"Archivo creado"})
                                except:
                                    sendInfo(conn,{"message":"Error al crear archivo"}) 
                            elif res["opt"] == 4:
                                try:
                                    directory = initialPath+res["path"]+"/"+res["fileName"]
                                    fileSize = res["fileSize"]
                                    fileZip = directory+".zip"
                                    file = open(fileZip,"wb")
                                    
                                    for i in range(0,fileSize//BUFFER_SIZE+1):
                                        bytes_read = conn.recv(BUFFER_SIZE)
                                        file.write(bytes_read)

                                    file.close()
                                    
                                    os.makedirs(directory, exist_ok=True)
                                    shutil.unpack_archive(fileZip, directory, "zip")
                                    os.remove(fileZip)

                                    sendInfo(conn,{"message":"Carpeta creada"})
                                except Exception as e:
                                    print(e)
                                    sendInfo(conn,{"message":"Error al crear carpeta"})
                            elif res["opt"] == 7:
                                path = initialPath+res["path"]+"/"+res["directoryName"]
                                os.makedirs(path, exist_ok=True)
                                sendInfo(conn,{"message":"Carpeta creada correctamente"})
                        else:
                            break
            finally:
                print('Se cerró la conexión con', addr)
                conn.close()

# shutil.unpack_archive(filename, extract_dir, archive_format)

if __name__ == "__main__":
    socketServidor()
    

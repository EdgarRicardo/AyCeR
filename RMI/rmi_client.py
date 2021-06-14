import Pyro5.api
import json
import threading
from socketsClass import SocketsMultibroadcast
from pprint import pprint
import base64

s = SocketsMultibroadcast()
rmiBusqueda = []
fileSearch = {}

def receive():
    while True:
        try:
            data, address = s.sockLectura.recvfrom(1024)
            message = json.loads(data.decode('utf-8'))
            if 'rmi' in message:
                rmiBusqueda.append(message["rmiCode"])
            if 'close' in message:
                rmiBusqueda.remove(message["rmiCode"])
            #threads.append(threading.Thread(target=sendFile))
        except Exception as e:
            print("Error!")
            print(e)
            s.closeSocketLectura()
            print("Socket de Lectura Cerrado")
            break

def getFilePart(rmiCode,filename,part,partsN): 
    global fileSearch
    search = Pyro5.api.Proxy(rmiCode) #Proxy direct name 
    partFile = search.getFilePart(filename,part,partsN)
    fileSearch[part] = base64.b64decode(partFile["data"])

def search():
    name = ''
    print('Esperando un RMI de busqueda')
    #pprint(rmiBusqueda)
    while True:
        rmiFile = []
        if(len(rmiBusqueda)>0):
            print('RMI disponibles: '+str(rmiBusqueda))
            name = input("Archivo a buscar? ").strip()
            if name == 'salir':
                break

            for rf in rmiBusqueda:
                try:
                    search = Pyro5.api.Proxy(rf) #Proxy direct name   
                    exists = search.search(name)
                    if exists:
                        rmiFile.append(rf)
                except:
                    print("Servidor ya no disponible: "+rf)
                    rmiBusqueda.remove(rf)
                    pass
            print('RMI con archivo buscado: '+str(rmiFile))
            threads = []
            i = 0
            for rf in rmiFile:    
                threads.append(threading.Thread(target=getFilePart, args=(rf,name, i,len(rmiFile))))
                i+=1
            [t.start() for t in threads] 
            [t.join() for t in threads]

            if(len(rmiFile)>0):
                fileD = open("./downloads/"+name,"wb")
                for i in range(0,len(rmiFile)):
                    fileD.write(fileSearch[i])
                fileD.close()
                print("Archivo Descargado de "+str(len(rmiFile))+ " servidor(es)")



if __name__ == "__main__":

    toSend = {
		"getRMI": True
	}
    toSend = json.dumps(toSend) 
    s.sockEscritura.sendto(toSend.encode('utf-8'), (s.IP_A, s.PORT))

    threads = []
    threads.append(threading.Thread(target=receive))
    threads.append(threading.Thread(target=search))
    [t.start() for t in threads] 
import socket
import struct
import sys
import json
from socketsClass import SocketsMultibroadcast

s = SocketsMultibroadcast()
listUsers = {}
# Receive/respond loop
while True:
    try:
        data, address = s.sockLectura.recvfrom(1024)
        message = json.loads(data.decode('utf-8'))
        # Solo actuar en caso del que mensaje sea de login
        if "login" in message:
            try:
                if(message["login"]):
                    users = list(listUsers.values())
                    data = {}
                    data["msg"] = "Usuarios conectados: " + str(users)
                    toSend = json.dumps(data) 
                    # sent = s.sockLectura.sendto(toSend.encode('utf-8'), (s.IP_A, s.PORT))
                    sent = s.sockLectura.sendto(toSend.encode('utf-8'), address)
                    listUsers[str(address)] = message["msg"]
                else:
                    del listUsers[str(address)]
                print(listUsers)
            except Exception as e:
                print("Error!")
                print(e)
                s.closeSocketEscritura()
                print("Socket de Escritura Cerrado")
                break
    except Exception as e:
        print("Error!")
        print(e)
        s.closeSocketLectura()
        print("Socket de Lectura Cerrado")
        break

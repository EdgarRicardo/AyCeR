import random
from random import randint
import pprint

size = 15

class Sopa():
    def posicionarPalabra(self,word,sopa,datosPalabras):
        x = randint(0,size)
        y = randint(0,size)
        while True:
            if word[0] == sopa[x][y] or sopa[x][y] == "":
                break
            x = randint(0,size)
            y = randint(0,size)
        
        flag = True
        possible = self.posibleDireccion(sopa,word,x,y)
        if possible:
            xf,yf = self.forDirecccion(sopa,word,possible,x,y,True)
            """ datosPalabras[word] = {
                "inicio": str(x)+","+str(y),
                "fin": str(xf)+","+str(yf)
            } """
            datosPalabras[str(x)+","+str(y)+":"+str(xf)+","+str(yf)] = word
        else:
            self.posicionarPalabra(word,sopa,datosPalabras)
            

    def posibleDireccion(self,sopa,word,x,y):
        flag = False
        # Derecha -> 1
        if y+len(word) <= size:
            if self.forDirecccion(sopa,word,1,x,y):
                return 1
        # Izquierda -> 2
        if y-len(word)-1 >= 0:
            if self.forDirecccion(sopa,word,2,x,y):
                return 2

        # Arriba -> 3
        if x+len(word) <= size:
            if self.forDirecccion(sopa,word,3,x,y):
                return 3
        # Abajo -> 4
        if x-len(word) >= 0:
            if self.forDirecccion(sopa,word,4,x,y):
                return 4

        # Diagonal superior -> 5
        if x-len(word) >= 0 and y+len(word) <= size:
            if self.forDirecccion(sopa,word,5,x,y):
                return 5

        # Diagonal inferior -> 6
        if x+len(word) <= size and y-len(word) >= 0:
            if self.forDirecccion(sopa,word,6,x,y):
                return 6
        
        return 0


    def forDirecccion(self,sopa,word,direccion,x,y,modificarSopa = False):
        mx = 0
        my = 0

        if modificarSopa:
            for i in range(0,len(word)):
                sopa[x+mx][y+my] = word[i]
                if i != len(word) - 1:
                    if direccion in [1,5]:
                        my += 1
                    elif direccion in [2,6]:
                        my -= 1
                    elif direccion in [3,6]:
                        mx += 1
                    elif direccion in [4,5]:
                        mx -= 1
            return x+mx,y+my
        else:
            for i in range(0,len(word)):
                if word[i] != sopa[x+mx][y+my] and sopa[x+mx][y+my] != "":
                    return False
                if direccion in [1,5]:
                    my += 1
                elif direccion in [2,5]:
                    my -= 1
                elif direccion in [3,6]:
                    mx += 1
                elif direccion in [4,6]:
                    mx -= 1
        return True

    def printSopa(self,sopa):
        print(" ", end = "\t")
        for x in range(size+1):
            print(x, end = "\t")
        print('') 
        for x in range(size+1):
            print(x, end = "\t") 
            for y in range(size+1):
                print(sopa[x][y], end = "\t")
            print('')
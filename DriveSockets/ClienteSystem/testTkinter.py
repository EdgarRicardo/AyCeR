from tkinter import filedialog
from tkinter import *
import shutil
import os

# try:
# 	root = Tk()
# 	root.withdraw() # Quitar ventana de tkinter
# 	directory = filedialog.askdirectory(initialdir = ".",title = "Selelecciona la carpeta")
# 	print(directory)
# 	archivo_zip = shutil.make_archive("carpetaToSend","zip",directory)
# 	print(archivo_zip)
# 	file = open(archivo_zip,"rb")
# 	bytesFile = file.read()
# 	print(bytesFile)
# 	file.close()
# 	os.remove(archivo_zip)
# except Exception as e:
# 	print(e)
# 	print("Error al cargar archivo")

file =  filedialog.askopenfile(mode="rb",initialdir = ".",title = "Selelecciona tu archivo")
print (file.read())


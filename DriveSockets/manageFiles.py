import json
import os

class ManageFiles():
	
	def __init__(self):
		super().__init__()

	def getFiles(path):
		res = {}
	    for (dirpath, dirnames, filenames) in os.walk("."):
	        res["directorios"] = dirnames
	        res["archivos"] = filenames
	        break
	    return res

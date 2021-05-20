import requests
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor
import os
import threading
from requests.exceptions import HTTPError
from bs4 import BeautifulSoup
from pprint import pprint

visitados = []
pool = ThreadPoolExecutor(max_workers=30)
etiquetasToFound = ['img','a','style']

def analyseHTML(linkO,html,url):
	#Caso 1: /dddd/ddd -> url + linkFound -> listToCheck
	#Caso 2: ddddd/dddd -> url + /linkFound -> listToCheck
	#Caso 3: https://sdfdfdfssdfsdf.xxx/fcfasff -> listToCheck
	# http://dfsdfsdfsdf.ccc/sdfsdfsdf/dfdfsdf -> listToCheck
	#listToCheck = ["https://www.cdc.gov/coronavirus/2019-ncov/testing/index.html","http://www.google.com/","http://www.researchgate.net/profile/M_Gotic/publication/260197848_Mater_Sci_Eng_B47_%281997%29_33/links/0c9605301e48beda0f000000.pdf"]
	# Edgar's code
	# urlSplit = linkO.split("/")[0:3]
	# url = "/".join(urlSplit)
	listToCheck = []
	soup = BeautifulSoup(html)
	for etiqueta in etiquetasToFound:
		for link in soup.findAll(etiqueta):
			urlFound = None
			if link.get('href'):
				urlFound = link.get('href')
			elif link.get('src'):
				urlFound = link.get('src')

			if urlFound:
				if 'http' in urlFound:
					if url in urlFound:
						listToCheck.append(urlFound)
				elif urlFound[0] == "/":
					listToCheck.append(url+urlFound)
				else:
					listToCheck.append(url+"/"+urlFound)

				""" if linkO[-1] == "/":
					if urlFound[0] == "/":
						listToCheck.append(linkO+urlFound[1:-1])
					else:
						listToCheck.append(linkO+urlFound)
				else:
					if urlFound[0] == "/":
						listToCheck.append(linkO+urlFound)
					else:
						listToCheck.append(linkO+"/"+urlFound) """

	#html.close()
	return listToCheck

def saveContentFile(content,directory,filename):
	os.makedirs(directory, exist_ok=True)
	file = open(filename,"wb")
	file.write(content)
	file.close()
	return True

def getFiles(link,urlO):
	global visitados
	global pool
	if(link not in visitados):
		visitados.append(link)
		try:
			listLinks = []
			res = requests.request("GET", link)
			splitLink = link.split('/')
			raiz = "./"+splitLink[2]+"/"
			filename  = raiz + "/".join(splitLink[3:])
			path  = raiz + "/".join(splitLink[3:-1])
			if('text/html' in res.headers['content-type']):
				print("HTML")
				if filename.split("/")[-1] == '':
					filename += "index.html"
					path  = raiz + "/".join(splitLink[3:])
				elif 'htm' not in filename.split("/")[-1]:
					filename += "/index.html"
					path  = raiz + "/".join(splitLink[3:])
				saveContentFile(res.content,path,filename)
				listLinks = analyseHTML(link,res.content,urlO)
			else:
				print("File")
				saveContentFile(res.content,path,filename)

			print("Directory: "+ path)
			print("Filename: "+filename)

			return listLinks

		except HTTPError as http_err:
			print(f'HTTP error: {http_err}')
		except Exception as err:
			print(f'Error: {err}')
	return []

def poolThreads(listLinks,urlO):
	global pool
	the_futures = []
	for link in listLinks:
		future = pool.submit(getFiles, link,urlO)
		the_futures.append(future)
	for future in concurrent.futures.as_completed(the_futures):
		poolThreads(future.result(),urlO)


if __name__ == "__main__":
	#link = input("¿Dame tu link?: ")
	#link = "http://www.researchgate.net/profile/M_Gotic/publication/260197848_Mater_Sci_Eng_B47_%281997%29_33/links/0c9605301e48beda0f000000.pdf"
	#link = "https://www.cdc.gov/coronavirus/2019-ncov/testing/index.html"
	link = "https://www.cecyt3.ipn.mx/"
	urlSplit = link.split("/")[0:3]
	urlOriginal = "/".join(urlSplit)
	listLinks = getFiles(link,urlOriginal)
	poolThreads(listLinks,urlOriginal)


	

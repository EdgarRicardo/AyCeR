from typing import List
import requests
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor
import os
import threading
from requests.exceptions import HTTPError 
from selectolax.parser import HTMLParser 

visitados = []
pool = ThreadPoolExecutor(max_workers=30)

def extract(content):
    links = []
    dom = HTMLParser(content)
    for tag in dom.tags('a'):
        attrs = tag.attributes
        if 'href' in attrs:
            links.append(attrs['href'])
    
    for tag in dom.tags('img'):
        attrs = tag.attributes
        if 'href' in attrs:
            links.append(attrs['href'])

    return links


def analyseHTML(link,filename):
	urlSplit = link.split("/")[0:3]
	url = "/".join(urlSplit)
	listToCheck = []
	html = open(filename,"r",encoding="iso-8859-1")
	content = html.read()
	html.close()
	listaAux = extract(content)
	for elemento in  listaAux:
		if elemento[0:4] != "http":
			if elemento[0] == '/':
				listToCheck.append(url + elemento)
			else:
				listToCheck.append(url + '/' + elemento)
		else:
			listToCheck.append(elemento)
	return listToCheck

def saveContentFile(content,directory,filename):
	os.makedirs(directory, exist_ok=True)
	file = open(filename,"wb")
	file.write(content)
	file.close()
	return True

def getFiles(link):
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
				listLinks = analyseHTML(link,filename)
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

def poolThreads(listLinks):
	global pool
	the_futures = []
	for link in listLinks:
		future = pool.submit(getFiles, link)
		the_futures.append(future)
	for future in concurrent.futures.as_completed(the_futures):
		poolThreads(future.result())

if __name__ == "__main__":
	#link = input("¿Dame tu link?: ")
	link = "http://www.researchgate.net/profile/M_Gotic/publication/260197848_Mater_Sci_Eng_B47_%281997%29_33/links/0c9605301e48beda0f000000.pdf"
	link = "https://es.wikipedia.org/wiki/Page"
	link = "https://www.cdc.gov/coronavirus/2019-ncov/testing/index.html"
	#link = "http://www.google.com/"
	listLinks = getFiles(link)
	poolThreads(listLinks)


	

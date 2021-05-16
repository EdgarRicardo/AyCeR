from typing import List
import requests
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor
import os
import threading
from requests.exceptions import HTTPError  
from html.parser import HTMLParser
import sys

visitados = []
pool = ThreadPoolExecutor(max_workers=30)


'''class LinkParser(HTMLParser):
    def handle_starttag(self, tag, attrs): 
        if tag == 'a':
            for attr in attrs:
                if attr[0] == 'href':
                    self.links.append(attr[1])'''

class URLHtmlParser(HTMLParser):
    links = []
    
    def handle_starttag(self, tag, attrs):
        if tag != 'a':
            return
           
        for attr in attrs:
               if 'href' in attr[0]:
                   self.links.append(attr[1])
                   break

def analyseHTML(link,filename):
	#Caso 1: /dddd/ddd -> url + linkFound -> listToCheck
	#Caso 2: ddddd/dddd -> url + /linkFound -> listToCheck
	#Caso 3: https://sdfdfdfssdfsdf.xxx/fcfasff -> listToCheck
	# http://dfsdfsdfsdf.ccc/sdfsdfsdf/dfdfsdf -> listToCheck
	#listToCheck = ["https://www.cdc.gov/coronavirus/2019-ncov/testing/index.html","http://www.google.com/","http://www.researchgate.net/profile/M_Gotic/publication/260197848_Mater_Sci_Eng_B47_%281997%29_33/links/0c9605301e48beda0f000000.pdf"]
	urlSplit = link.split("/")[0:3]
	url = "/".join(urlSplit)
	listToCheck = []
	html = open(filename,errors='ignore')
	content = html.read()
	parser = URLHtmlParser()
	parser.feed(content)

	for elemento in parser.links:
		if elemento[0:4] != "http":
			if elemento[0] == '/':
				listToCheck.append(url + elemento)
			else:
				listToCheck.append(url + '/' + elemento)
		else:
			listToCheck.append(elemento)
	print(listToCheck)
	html.close()
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
	link = "http://www.google.com/"
	listLinks = getFiles(link)
	poolThreads(listLinks)


	

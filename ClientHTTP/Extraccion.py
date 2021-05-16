from __future__ import print_function
import urllib3, sys
from HTMLParser import HTMLParser
 
links = []
 
class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        if tag != 'a':
            return
        attr = dict(attrs)
        links.append(attr)
 
def extract(url):
 
    try:
        f = urllib3.urlopen(url)
        html = f.read()
        f.close()
    except urllib3.HTTPError as e:
        print(e, 'while fetching', url)
        return
 
    parser = MyHTMLParser()
    parser.links = []
    parser.feed(html)
    for l in links:
        print(l)
 
extract("http://www.google.com/")
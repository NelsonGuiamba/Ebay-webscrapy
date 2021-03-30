import re
from bs4 import BeautifulSoup as Bs
import requests
class WebSite:
	def __init__(self,searchUrl,seclass,setag,**kwards):
		self.search = searchUrl
		self.dict = {}
		self.seclass = seclass
		self.setag = setag
		for k,v in kwards.items():
			self.dict[k[2:]] = v
			
class Scraper:
	def __init__(self,web):
		self.site = web
	def crawl(self,item=None,local=False,html=None):
		if not local:
			r = requests.get(self.site.search+item)
			self.bs = Bs(r.text,'html.parser')
		else:
			self.bs = Bs(html,'html.parser')
		l = []
		d = {}
		divs = self.bs.find_all(self.site.setag,
		class_=self.site.seclass)[1:]
		for tag in divs:
			for k,v in self.site.dict.items():
				try:
					aux = tag.find(class_=re.compile(v)).getText()
				except:
					print(f'Dado nao encontrado {v}')
					aux = 'NULL'
				d[v] = aux
			l.append(d.copy())
			
		return l
		

ebay = WebSite("https://www.ebay.com/sch/i.html?_from=R40&_trksid=m570.l1313&_nkw=",
seclass='s-item__wrapper clearfix',
setag='div',
seprice='s-item__price',
selocal='s-item__itemLocation',
sejuros='s-item__logistic')

scrap = Scraper(ebay)
result = scrap.crawl(item='Iphone+9')

import csv

with open('names.csv', 'w', newline='') as csvfile:
    fieldnames = list(result[0].keys())
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for di in result:
    	writer.writerow(di)

#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from APIserver import apiServer
import urllib3
import requests

def get_full_text(page):
	for script in page(['style', 'script', '[document]', 'head', 'title', 'meta']):
	    script.extract() 
	text = page.get_text()
	# break into lines and remove leading and trailing space on each
	lines = (line.strip() for line in text.splitlines())
	# break multi-headlines into a line each
	chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
	# drop blank lines
	text = '\n'.join(chunk for chunk in chunks if chunk)
	return text

http = urllib3.PoolManager()
print "1"
# urlopen = http.request('GET', "https://www.moneysupermarket.com/car-leasing/", timeout=3)
urlopen = http.request('GET', 'http://httpbin.org/robots.txt', timeout=3)
# urlopen = requests.get('http://httpbin.org/robots.txt')
print "2"
print "status",urlopen.status
# print "status 2",requests.codes.ok
print "3"
soup = BeautifulSoup(urlopen.data, "html.parser")
# soup = BeautifulSoup(urlopen, "html.parser")
print "4"
print "----------text------"
print get_full_text(soup)
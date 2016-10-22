#!/usr/bin/env python
# -*- coding: utf-8 -*-
from APIserver import apiServer
import re

def check_word(query, line):
    count = 0
    for q in query.split(' '):
        print line,"###",q,"###", q.lower() in line.lower()
        if q.lower() in line.lower():
            count += 1
    max = len(query.split(' '))
#     print count, max, count/max
    return count/max

def check_optz(query, line):
    if query.lower() in line.lower():
        return 1/1.0
    else:
        data = check_word(query,line)
        return data/2.0

def pretty_line(text):
    line = re.sub('[^a-zA-Z0-9-á-ú_*.]', ' ', str(text))
    line = re.sub('[!@#${}()/&--%"¿¡*,.]', ' ' , line)
    line = ' '.join(line.split())
    return line

pageOptz = apiServer.get_page_optz()
idPositions = int(pageOptz["idPositions"])
# print "original", pageOptz["query"]
query = pretty_line(pageOptz["query"])
url = pretty_line(pageOptz["url"])
# print url
optz = check_optz(query, url)
# print optz
# print "fixed", query
# print idPositions
data = apiServer.get_page_data(idPositions)
for a in data:
    if a["type"] == "h1":
        line = pretty_line(a["text"])
        print "h1","###", a["text"],"###", line
        optz = check_optz(query, line)
        print "h1 #optz#", optz
    elif a["type"] == "h2":
        line = pretty_line(a["text"])
        print "h2","###", a["text"],"###", line
        optz = check_optz(query, line)
        print "h2 #optz#", optz
    elif a["type"] == "img":
        line = pretty_line(a["text"])
        print "img","###", a["text"],"###", line
        optz = check_optz(query, line)
        print "img #optz#", optz
    elif a["type"] == "title":
        line = pretty_line(a["text"])
        print "title","###", a["text"],"###", line
        optz = check_optz(query, line)
        print "title #optz#", optz
    

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
    print count, max, count/max
    return count/max

def pretty_line(text):
    line = re.sub('[^a-zA-Z0-9-á-ú_*.]', ' ', str(text))
    line = re.sub('[!@#${}()/&--%"¿¡*,.]', ' ' , line)
    line = ' '.join(line.split())
    return line

pageOptz = apiServer.get_page_optz()
idPositions = int(pageOptz["idPositions"])
# print "original", pageOptz["query"]
query = pretty_line(pageOptz["query"])
# print "fixed", query
# print idPositions
data = apiServer.get_page_data(idPositions)
for a in data:
    if a["type"] == "h1":
        line = pretty_line(a["text"])
        print "h1","###", a["text"],"###", line
        optz = check_word(query, line)
    elif a["type"] == "h2":
        line = pretty_line(a["text"])
        print "h2","###", a["text"],"###", line
        optz = check_word(query, line)
    elif a["type"] == "img":
        line = pretty_line(a["text"])
        print "img","###", a["text"],"###", line
        optz = check_word(query, line)
    elif a["type"] == "title":
        line = pretty_line(a["text"])
        print "title","###", a["text"],"###", line
        optz = check_word(query, line)
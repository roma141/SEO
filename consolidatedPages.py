#!/usr/bin/env python
# -*- coding: utf-8 -*-
from APIserver import apiServer
import re

def page_optz():
    def check_word(query, line):
        count = 0.0
        for q in query.split(' '):
            if q.lower() in line.lower():
                count += 1
        max = len(query.split(' '))
        return count/max
    
    def check_optz(query, line):
        if query.lower() in line.lower():
            return 1/1.0
        else:
            data = check_word(query,line)
            return data/2.0
    
    def pretty_line(text):
        line = re.sub('[^a-zA-Z0-9-á-ú_*.]', ' ', str(text))
        line = re.sub('[!@#${}()/&--%"¿¡*,._]', ' ' , line)
        line = ' '.join(line.split())
        return line
    
    pageOptz = apiServer.get_page_optz()
    idPositions = int(pageOptz["idPositions"])
    query = pretty_line(pageOptz["query"])
    rawUrl = pageOptz["url"]
    url = pretty_line(pageOptz["url"])
    optzTitle = 0.0
    optzUrl = 0.0
    optzUrl = check_optz(query, url)
    data = apiServer.get_page_data(idPositions)
    h1c = 0
    h1 = 0.0
    noH1 = 0
    for a in data:
    #     print a["type"]
        if a["type"] == "h1":
            line = pretty_line(a["text"])
            h1 += check_optz(query, line)
            h1c += 1
            noH1 = 1
        elif a["type"] == "h2":
            line = pretty_line(a["text"])
            optz = check_optz(query, line)
        elif a["type"] == "img":
            line = pretty_line(a["text"])
            optz = check_optz(query, line)
        elif a["type"] == "title":
            line = pretty_line(a["text"])
            optzTitle = check_optz(query, line)
    
    if noH1 < 0:    
        if h1c < 1:
            optzH1 = h1/(h1c * 2.0)
        else:
            optzH1 = h1
    else:
        optzH1 = h1
    domain = ["com","org","edu","uk","co", "index.html", "index"]
    pageDomain = []
    urlDomain = 0.0
    a = rawUrl.lower()
    
    if a.endswith("/"):
        a = a[:-1]
    if a.endswith("//"):
        a = a[:-2]
    for t in domain:
        if a.endswith(t):
            urlDomain = 1.0
    
    apiServer.save_page_optz(idPositions, urlDomain, optzUrl, optzTitle, optzH1, (urlDomain + optzUrl + optzTitle + optzH1))

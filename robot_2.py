#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pageCrawl
import consolidatedPages
# import time
import sys  

reload(sys)  
sys.setdefaultencoding('utf8')

c = 0
while True:
#     time.sleep(2)
    print "round", c
    if c == 30: 
        break 
    try:
        pageCrawl.page_crawl()
        consolidatedPages.page_optz()
    finally:
        c += 1
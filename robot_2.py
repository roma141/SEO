#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pageCrawl
import consolidatedPages
# import time
import sys  

reload(sys)  
sys.setdefaultencoding('utf8')

c = 0
print "robot 2"
while True:
#     time.sleep(2)
    print "round", c
    if c == 30: 
        break 
    try:
        pageCrawl.page_crawl()
    except:
    	print "error page_crawl"
    try:
    	consolidatedPages.page_optz()
    except Exception as e:
    	print "error page_optz"
    	print e
    finally:
        c += 1
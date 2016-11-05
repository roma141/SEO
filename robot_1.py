#!/usr/bin/env python
# -*- coding: utf-8 -*-
import checkQuery
import googleQuery
import time
import sys  

reload(sys)  
sys.setdefaultencoding('utf8')

c = 0
while True:
	print c
	time.sleep(2)
	if c == 10:
	    break 
	try:
	    checkQuery.check_query()
	    googleQuery.google_search()
	finally:
	    c += 1
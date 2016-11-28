#!/usr/bin/env python
# -*- coding: utf-8 -*-
import checkQuery
import googleQuery
# import time
import sys
# import random

reload(sys)  
sys.setdefaultencoding('utf8')

c = 0
while True:
	print c
	# time.sleep(round(random.uniform(7,13),1))
	if c == 30:
	    break 
	try:
	    checkQuery.check_query()
	    googleQuery.google_search()
	except IOError as e:
		print "I/O error({0}): {1}".format(e.errno, e.strerror)
	except ValueError:
	    print "Could not convert data to an integer."
	except:
	    print "Unexpected error:", sys.exc_info()[0]
	finally:
	    c += 1
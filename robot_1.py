#!/usr/bin/env python
# -*- coding: utf-8 -*-
import checkQuery
import googleQuery
# import time
import sys
# import random

reload(sys)  
sys.setdefaultencoding('utf8')

print "robot 1"
c = 0
while True:
	print c
	# time.sleep(round(random.uniform(7,13),1))
	if c == 30:
	    break 
	try:
		print "check_query"
		# checkQuery.check_query()
	    # googleQuery.google_search()
	# except IOError as e:
	# 	print "check_query - I/O error({0}): {1}".format(e.errno, e.strerror)
	# except ValueError:
	#     print "check_query - Could not convert data to an integer."
	except:
		print ""
		print "check_query - Unexpected error:", sys.exc_info()[0]
	try:
	    # checkQuery.check_query()
	    print "google_search"
	    googleQuery.google_search()
	# except IOError as e:
	# 	print "google_search - I/O error({0}): {1}".format(e.errno, e.strerror)
	# except ValueError:
	#     print "google_search - Could not convert data to an integer."
	except:
	    print "google_search - Unexpected error:", sys.exc_info()[0]
	finally:
	    c += 1
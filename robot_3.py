#!/usr/bin/env python
# -*- coding: utf-8 -*-
import domainSeeker
import domainAuthority
# import time
import sys  

reload(sys)  
sys.setdefaultencoding('utf8')

c = 0
while True:
#     time.sleep(2)
    print "round", c
    if c == 2:
        break 
    try:
        domainSeeker.domain_seeker()
    except:
    	print "error domain_seeker"
	try:
		domainAuthority.domain_authority()
	except:
		print "error domain_authority"
    finally:
        c += 1
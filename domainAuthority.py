#!/usr/bin/env python
# -*- coding: utf-8 -*-
from APIserver import apiServer
# import sys

# reload(sys)
# sys.setdefaultencoding('utf8')

def domain_authority():
	d = 0
	cPos = apiServer.get_count_positions()
	cDoms = apiServer.get_count_domain()
	if cPos and cDoms:
		for cDom in cDoms:
			print "domain authority done %", (d*100.0)/len(cDoms)
			# print cDom["c"], cPos
			authority = cDom["c"]*1.0/cPos
			# print "authority", authority
			apiServer.save_domain_authority(cDom["idDomain"], authority)
			d += 1
#!/usr/bin/env python
# -*- coding: utf-8 -*-
from APIserver import apiServer
# import sys

# reload(sys)
# sys.setdefaultencoding('utf8')

def domain_seeker():
	d = 0
	urls = apiServer.get_url_for_domain()
	if urls:
		for url in urls:
			# print url["idPositions"]
			print "domain check done %", (d*100.0)/len(urls)
			one = url["url"]
			if "http://" in one:
				temp = one.replace("http://","")
			elif "https://" in one:
				temp = one.replace("https://","")
			indx = temp.index("/")
			real = temp[0:indx]
			# print real
			data = apiServer.check_domain(real)
			if data:
				# print "true"
				# print "check_domain", data
				apiServer.update_consolidate(url["idPositions"], int(data["id"]))
			else:
				# print "false"
				apiServer.add_domain(real)
			d += 1
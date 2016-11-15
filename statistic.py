#!/usr/bin/env python
# -*- coding: utf-8 -*-
from APIserver import apiServer
import sys

reload(sys)
sys.setdefaultencoding('utf8')

def statistic_maker(a):
	a = float(a)
	if a > 4:
		return "nightmare"
	elif a > 3:
		return "hardcore"
	elif a > 2:
		return "hard"
	elif a > 1:
		return "medium"
	elif a > 0:
		return "easy"

data  = apiServer.get_data_terms()
statistic = {}
c = 0
m = len(data)
if data:
	for t in data:
		normal = {"nightmare":0,"hardcore":0,"hard":0,"medium":0,"easy":0}
		print "#", c+1,"-", round(c*100.0/m, 2), "%"
		if statistic:
			if statistic.has_key(str(t["idTerm"])):
				dif = statistic_maker(t["score"])
				statistic[str(t["idTerm"])][dif] += 1
			else:
				statistic[str(t["idTerm"])] = normal
				dif = statistic_maker(t["score"])
				statistic[str(t["idTerm"])][dif] += 1
		else:
			statistic[str(t["idTerm"])] = normal
			dif = statistic_maker(t["score"])
			statistic[str(t["idTerm"])][dif] += 1

		c += 1
	apiServer.save_statistic(statistic)
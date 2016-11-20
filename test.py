#!/usr/bin/env python
# -*- coding: utf-8 -*-
from APIserver import apiServer
import re

def pretty_line(text):
        line = re.sub('[^a-zA-Z0-9-á-ú_*.]', ' ', str(text))
        line = re.sub('[!@#${}()/&--%"¿¡*,._]', ' ' , line)
        line = ' '.join(line.split())
        return line
terms = apiServer.get_terms_for_vol()
total = ""
c = 0
for t in terms:
	if c == 0:
		total = pretty_line(t["term"])
	else:
		total = total + ","+ pretty_line(t["term"])
	c += 1

# print total
# import random
# for a in xrange(0,100):
# 	print round(random.uniform(7,13),1)
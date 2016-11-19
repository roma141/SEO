#!/usr/bin/env python
# -*- coding: utf-8 -*-
from APIserver import apiServer
import csv
import codecs
import os

cwd = os.getcwd()
path = cwd + "/temp"
list = os.listdir(path)
# time_sorted_list = sorted(list, key=os.path.getmtime)
# file_name = time_sorted_list[len(time_sorted_list)-1]
full_path = path + "/" + list[0]
data = []
f = codecs.open(full_path, 'rb',"utf-16")
reader=csv.DictReader(f,delimiter='\t')
for row in reader:
	a = row["Keyword"]
	b = row["Avg. Monthly Searches (exact match only)"]
	if b == "":
		b = 0
	line ={"Keyword":a,"Searches":b}
	data.append(line)
f.close()
# print data
apiServer.save_terms_searchs(data)
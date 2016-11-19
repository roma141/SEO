#!/usr/bin/env python
# -*- coding: utf-8 -*-
from APIserver import apiServer
import csv
import codecs
import os

cwd = os.getcwd()
path = cwd + "/upload"
list = os.listdir(path)
# time_sorted_list = sorted(list, key=os.path.getmtime)
# file_name = time_sorted_list[len(time_sorted_list)-1]
if list:
	for file in list:
		print file
		full_path = path + "/" + file
		data = []
		f = codecs.open(full_path, 'rb',"utf-16")
		# print f.read()
		fi = f.read().encode("utf-8")
		reader=csv.reader(fi.splitlines(),delimiter='\t')
		# print reader
		list = []
		for row in reader:
			if len(row) > 1:
				list.append(row)
		for row in list:
			if row[1].lower() == "Palabra clave".lower():
				continue
			if row[1].lower() == " --".lower():
				continue
			# print ""
			# print row[1]
			data.append(row[1])
		f.close()
		# print data
		print len(data)
		apiServer.save_terms(data)
		# os.remove(full_path)
else:
	print "no file"
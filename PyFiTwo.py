import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import csv
import os
import collections as cl

script_dir = os.path.dirname(__file__)
csv_path = os.path.join(script_dir,'/CSV/WigleWifi_2018_0220.csv')

fileInitial = open('CSV/WigleWifi_2018_0220.csv','r')
fileReader = csv.reader(fileInitial,delimiter=',')
header = next(fileReader)		# skip the device-metadata line.
header = next(fileReader)


fiDict = dict()
fiList = []

for row in fileReader:
	MAC = row[0]
	GPS = [row[6],row[7]]
	fiList.append([MAC,GPS])


for item in fiList:
	
	if item[0] in fiDict.keys():
		fiDict[item[0]].append([item[1][0],item[1][1]])
	else:
		fiDict[item[0]] = ([item[1][0],item[1][1]])
	


for item in fiDict:
	print(str(fiDict[item]) + '\n')
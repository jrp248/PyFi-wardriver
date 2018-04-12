import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import csv
import os
import collections as cl
import datetime as dt
import pandas as pd


script_dir = os.path.dirname(__file__)
csv_path = os.path.join(script_dir,'/CSV/WigleWifi_2018_0220.csv')

fileInitial = open('CSV/WigleWifi_2018_0220.csv','r')
fileReader = csv.reader(fileInitial,delimiter=',')
header = next(fileReader)		# skip the device-metadata line.
header = next(fileReader)		# read relevant categories in.


fiDict = dict()	# pre-allocate.
fiList = []
fiTime = []
fiMAC = []
# extract meta-data with the builtin CSV reader.
for row in fileReader:
	MAC = row[0]
	GPS = [row[6],row[7]]
	UTC = row[3]
	fiList.append([MAC,GPS])
	fiTime.append([MAC,UTC])
	fiMAC.append(MAC)


# In this scenario, only extracting unique MACs from list.
unique_MAC = []
for x in fiMAC:
	if x not in unique_MAC:
		unique_MAC.append(x)

print('Unique Addresses: ',len(unique_MAC))

# removing datestamp and rewriting the fiTime list.
for item in fiTime:
	TimeSplit = item[1].split(" ")
	item[1] = TimeSplit[1]

# Rather, it may be more beneficial to perform time operations in a single
# comparison loop of the numPy matrix/hash table created by M.

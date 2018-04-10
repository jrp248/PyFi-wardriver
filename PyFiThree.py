import numpy as np
import scipy as sp
import csv, os
import collections as cl
import pandas as pd
from functools import partial
import matplotlib.pyplot as plt
import datetime as dt

script_dir = os.path.dirname(__file__)
csv_path = os.path.join(script_dir,'/CSV/WigleWifi_2018_0220.csv')

fileInitial = open('CSV/WigleWifi_2018_0220.csv','r')
fileReader = csv.reader(fileInitial,delimiter=',')
header = next(fileReader)		# skip the device-metadata line.
header = next(fileReader)		# read relevant categories in.

fiDict = dict()	# pre-allocate.
fiList = []
fiTime = []

# extract meta-data with the builtin CSV reader.
for row in fileReader:
	MAC = row[0]
	GPS = [row[6],row[7]]
	UTC = row[3]
	fiList.append([MAC,GPS])
	fiTime.append([MAC,UTC])

# Convert each GPS element to float.
for row in fiList:
	element = row[1][0:2]
	row[1][0] = float(element[0])
	row[1][1] = float(element[1])

MAC_count = cl.Counter(MAC)
print(MAC[7])


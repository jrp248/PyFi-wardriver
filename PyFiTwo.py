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
header = next(fileReader)		# read relevant categories in.


fiDict = dict()	# pre-allocate.
fiList = []

# extract meta-data with the builtin CSV reader.
for row in fileReader:
	MAC = row[0]
	GPS = [row[6],row[7]]
	fiList.append([MAC,GPS])



# sweep List, check if duplicate is present, append GPS data. If the
# entry isn't there, add it within the "else" statement.

for item in fiList:	
	if item[0] in fiDict.keys():
		fiDict[item[0]].append([item[1][0],item[1][1]])
	else:
		fiDict[item[0]] = ([item[1][0],item[1][1]])
	

#for item in fiDict:
#	print(str(fiDict[item]) + '\n')


print(fiList[5][0]) # <- figure out how to properly access the MAC addresses.

# plot the histogram for the data to show concentration.
#plt.bar(range(len(MAC_count)),MAC_count.values(),align="center")
#plt.xticks(range(len(MAC_count)), MAC_count.keys())
#plt.xticks(rotation=70)
#plt.xlabel('MAC Addresses')
#plt.ylabel('Frequency')
#plt.show()
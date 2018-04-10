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

# Convert each GPS element to float.
#for row in fiList:
#	element = row[1][0:2]
#	row[1][0] = float(element[0])
#	row[1][1] = float(element[1])






# sweep List, check if duplicate is present, append GPS data. If the
# entry isn't there, add it within the "else" statement.

for item in fiList:	
	if item[0] in fiDict.keys():
		fiDict[item[0]].extend([item[1][0],item[1][1]]) #! OR APPEND
	else:
		fiDict[item[0]] = ([item[1][0],item[1][1]])
	

"""
HISTOGRAM PLOTTING
"""

#for item in fiDict:
#	print(str(fiDict[item]) + '\n')
#print(fiList[5][0]) # <- figure out how to properly access the MAC addresses.
# plot the histogram for the data to show concentration.
#plt.bar(range(len(MAC_count)),MAC_count.values(),align="center")
#plt.xticks(range(len(MAC_count)), MAC_count.keys())
#plt.xticks(rotation=70)
#plt.xlabel('MAC Addresses')
#plt.ylabel('Frequency')
#plt.show()

"""
First, create fiDictTime containing MAC address keys and their corresponding
sliced UTC time values. Develop a function that accepts the UTC string, and provides
the datetime object instead. Find the time delta if the MAC addresses are unalike.
"""

# <- fiTime[0][1] returns the UTC. fiTime[0][0] returns MAC.
TimeSplit = fiTime[0][1].split(" ")
#print(TimeSplit[1])

TimeSplit = [] 	# temporary variable for splitting and R/W.


# removing datestamp, passing only the UTC hour:minute:second to second list entry.
for item in fiTime:
	TimeSplit = item[1].split(" ")
	item[1] = TimeSplit[1]

FirstTime = []
CompareTime = []
fiTimeMatrix = []
timedelt_original = dt.timedelta()
timedelt_compare = dt.timedelta()

# store each hour, minute and second locally, pass it to the timedelta object.
for item in fiTime:
	for comp_item in fiTime:
		if item[0] != comp_item[0]:
			# do stuff!
			FirstTime = item[1].split(":")
			CompTime = comp_item[1].split(":")
			timedelt_original = dt.timedelta(hours=int(FirstTime[0]),minutes=int(FirstTime[1]),seconds=int(FirstTime[2]))
			timedelt_compare = dt.timedelta(hours=int(CompTime[0]),minutes=int(CompTime[1]),seconds=int(CompTime[2]))
			diff = abs(timedelt_compare - timedelt_original)
			fiTimeMatrix.append([item[0], comp_item[0], diff])

# print(fiTimeMatrix[27][2]) 	# <- fiTimeMatrix Example.
MAC_count = cl.Counter(fiMAC)


# Inserting a new dictionary containing the average Latitude and Longitude per MAC address.
fiDict_avg = {}
TotalLat = []
TotalLong = []


# averaging the Lat/Long per item in the fiDict. If Latitude is odd, and Longitude is even...
for key, value in fiDict.items():	# iterating the GPS values.
	float_value = [float(i) for i in value]
	TotalLat = float_value[0::2]
	TotalLong = float_value[1::2]

	avg_Lat = np.mean(TotalLat)
	avg_Long = np.mean(TotalLong)
	fiDict_avg.update({key:[avg_Lat,avg_Long]})


"""
FOR EXPORTING TO GOOGLE FUSION TABLE FORMAT
"""

#for key, value in fiDict_avg.items():
#	print(key,value)
print('Raw Matrix: ',fiTimeMatrix[27][0:2])
#csv_output = []
#for key, value in fiDict_avg.items():
#	temp = [value[0],value[1],key]
#	csv_output.append(temp)
#df = pd.DataFrame(csv_output, columns=["Latitude","Longitude","MAC"])
#df.to_csv('Output/avgLocation.csv',index=False)


"""
MAKING TABLE OF  STRING VALUES.
"""

table_data = []
column_names = []
index_names = []

for item in fiTimeMatrix:
	table_data.append([str(item[0]),str(item[1]),str(item[2])])
	index_names.append(str(item[0]))

print('List Length: ',len(table_data))
print('List Entry: ',table_data[4])
print('\n')

"""
PERFORM A SIMILAR COMPARISON WHERE IF A COMPARISON
ITEM DOESN'T OCCUR, APPEND A NULL.
"""
# creating a hash table, with the index corresponding to the position in the
# numpy matrix.
#MACtoIndex = {}
#cnt = 0
#
# concern that fiMAC may not consolidate only relevant values.
#for addr in index_names:
#	if not addr in MACtoIndex:
#		MACtoIndex.update({addr:cnt})
#		cnt = cnt + 1
#
#
# creating full matrix.
#matrix = np.full((len(table_data),len(table_data)),np.nan)
#
#for entry in table_data:
#	empty[MACtoIndex[entry[0]]][MACtoIndex[entry[1]]] = entry[2]


# Boolean for duplicate checking.
def boolDupCheck(e1,e2):
	"""
	Determines if duplicates are present. e1 = [MAC1, MAC2, Time].
	"""
	if( (e1[0]==e2[0]) and (e1[1]==e2[1]) and (e1[2]==e2[2]) ) or ( (e1[0]==e2[1]) and (e1[1]==e2[0]) and (e1[2]==e2[2]) ):
		return True
	else:
		return False


table_data_no_dups = []

for e1 in table_data:
	found = False
	for e2 in table_data_no_dups:
		if (boolDupCheck(e1, e2)):
			found = True
			break
	if not found:
			table_data_no_dups.append(e1)
			print(len(table_data_no_dups)/len(table_data))
	if not table_data_no_dups:
		table_data_no_dups.append(e1) # initializes table if nothing is present. Second for-loop then starts.

print(len(table_data_no_dups))
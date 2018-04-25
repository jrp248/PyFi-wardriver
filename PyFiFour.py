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



# search through fiTime, using entries in unique_MAC. if an occurrence pops,
# add that time value to the new list. Afterwards, skip all other instances of that MAC address
# re-occurring. Compare for next unique_MAC.

unique_fiTime = []

for unique_item in unique_MAC:
	for comparison in fiTime:
		if unique_item == comparison[0]:
			unique_fiTime.append([unique_item, comparison[1]])
			break


print('Validate Size: ',len(unique_fiTime)) # validate its the same length as unique_MAC.

"""
Establishing the fiTimeMatrix. If the duplicates are present, make the time delta 0.
"""

fiTimeMatrix = []

FirstTime = []
CompTime = []
timedelt_original = dt.timedelta()
timedelt_compare = dt.timedelta()
zero_time = dt.timedelta(hours=0,minutes=0,seconds=0)

# make sure it's searching through uniqueMAC instead - append first time instance.

for item in unique_fiTime:
	for comp_item in unique_fiTime:
		if item[0] == comp_item[0]:
			fiTimeMatrix.append([item[0], comp_item[0], zero_time])
		else:
			FirstTime = item[1].split(":")
			CompTime = comp_item[1].split(":")
			timedelt_original = dt.timedelta(hours=int(FirstTime[0]),minutes=int(FirstTime[1]),seconds=int(FirstTime[2]))
			timedelt_compare = dt.timedelta(hours=int(CompTime[0]),minutes=int(CompTime[1]),seconds=int(CompTime[1]))
			diff = abs(timedelt_compare - timedelt_original)
			fiTimeMatrix.append([item[0], comp_item[0], diff])


print('Single Entry:',fiTimeMatrix[27][:])



"""
Creating the hash table for correct numpy indexing. Needs a fiTimeMatrix for searching.
Need the for loop that is going through and filling the numpy matrix to be an outer row search,
and the inner loop to be a column search.
"""

# Hashing operation.
index_names = []
table_data = []
column_names = []

# sifting through total fiTimeMatrix, assigning index and table_data.
for item in fiTimeMatrix:
	table_data.append([str(item[0]), str(item[1]),str(item[2])])
	index_names.append(str(item[0]))


# table_data times may not be symmetric. Perform boolean check for duplicates, then remove.
def boolCheck(e1,e2):
	"""
	Determines if duplicates are present. e1 = [MAC1, MAC2, Time]
	"""
	if(e1[0]==e2[1]) and (e1[1]==e2[0]):
		return True
	else:
		return False

# creating new table_data.
table_data_no_dups = []
print('Duplicate Removal. Length of initial Table: ',len(table_data))
print('Removing Duplicates...')
for e1 in table_data:
	found = False 		# starts with no duplicate found.
	for e2 in table_data_no_dups:
		if(boolCheck(e1,e2)):
			found = True
			break
	if not found:
		table_data_no_dups.append(e1)
	if not table_data_no_dups:
		table_data_no_dups.append(e1) 	# initializes table if nothing present.

print('Done.')



# dictionary that will assign the matrix position to a MAC address.
MACtoIndex = {}
cnt = 0

# adds the MAC address to the list if not present. Increments index counter.
for addr in index_names:
	if not addr in MACtoIndex:
		MACtoIndex.update({addr:cnt})
		cnt = cnt + 1

# formatting NumPy matrix.
matrix = np.zeros(shape=(len(unique_MAC),len(unique_MAC)),dtype=object)

# dimensionality check.
print('Matrix Dimensions: ',matrix.shape)
print('Assessing Organization of Table...')
print(table_data[0][:])
print(table_data[1][:])
print(table_data[1167][:])
str1 = 'f0:ab:54:bc:30:eb'
str2 = 'a0:63:91:a0:a5:33'
print(str1,' Hash Table Contents: ',MACtoIndex[str1])
print(str2,' Hash Table Contents: ',MACtoIndex[str2],'\n')

# actual table assignment.
for entry in table_data_no_dups:
	matrix[MACtoIndex[str(entry[0])]][MACtoIndex[str(entry[1])]] = entry[2]

print(' Numpy Matrix Contents:\n')
print(matrix)
quit()

"""
Now that the matrix is assembled, use the Hash Table Keys for the columns
and rows in the pandas dataframe.
"""

pd_matrix = pd.DataFrame(matrix, index=MACtoIndex.keys(), columns=MACtoIndex.keys())
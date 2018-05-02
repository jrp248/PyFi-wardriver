# Map_Parser Script.

import numpy as np
import scipy as sp
import pandas as pd
import csv
import os
import datetime as dt

file = open('CSV/GPS_Map.csv','r')
fileReader = csv.reader(file,delimiter=',')
header = next(fileReader)

csv_list = []
location_list = []

# String Location, float GPS.
for row in fileReader:
	Location = row[0]
	North = row[1]
	North = North.split(", ")
	North = [float(North[0]),float(North[1])]
	South = row[2]
	South = South.split(", ")
	South = [float(South[0]),float(South[1])]
	East = row[3]
	East = East.split(", ")
	East = [float(East[0]),float(East[1])]
	West = row[4]
	West = West.split(", ")
	West = [float(West[0]),float(West[1])]
	csv_list.append([Location,North,South,East,West])
	location_list.append(Location) # <- For use in Hash Table.


# Now, importing WiGLE database.
fileInitial = open('CSV/WigleWifi_2018_0220.csv','r')
fileReader = csv.reader(fileInitial,delimiter=',')
header = next(fileReader)		# skip the device-metadata line.
header = next(fileReader)		# read relevant categories in.


fiList = []
fiTime = []
fiMAC = []
fiDict = dict()

for row in fileReader:
	MAC = row[0]
	GPS = [row[6],row[7]]
	UTC = row[3]
	fiList.append([MAC,GPS])
	fiTime.append([MAC,UTC])
	fiMAC.append(MAC)

# Creating dictionary.
for item in fiList:	
	if item[0] in fiDict.keys():
		fiDict[item[0]].extend([item[1][0],item[1][1]]) #! OR APPEND
	else:
		fiDict[item[0]] = ([item[1][0],item[1][1]])

# removing datestamp, rewriting fiTime.
for item in fiTime:
	TimeSplit = item[1].split(" ")
	item[1] = TimeSplit[1]

# only extracting unique MACs from list.
unique_MAC = []
for x in fiMAC:
	if x not in unique_MAC:
		unique_MAC.append(x)

# Comparing for next unique MAC address.
unique_fiTime = []
for unique_item in unique_MAC:
	for comparison in fiTime:
		if unique_item == comparison[0]:
			unique_fiTime.append([unique_item, comparison[1]])
			break


# Establishing the fiTimeMatrix. If the duplicates are present, make the time delta 0.

fiTimeMatrix = []

FirstTime = []
CompTime = []
timedelt_original = dt.timedelta()
timedelt_compare = dt.timedelta()
zero_time = dt.timedelta(hours=0,minutes=0,seconds=0)

# Creating Entries of MAC and Timedeltas.
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

# Need the averaged GPS positions and MAC List for MAC to Location dictionary.
fiDict_avg = {}
TotalLat = []
TotalLong = []
for key, value in fiDict.items():	# iterating the GPS values.
	float_value = [float(i) for i in value]
	TotalLat = float_value[0::2]
	TotalLong = float_value[1::2]

	avg_Lat = np.mean(TotalLat)
	avg_Long = np.mean(TotalLong)
	fiDict_avg.update({key:[avg_Lat,avg_Long]})

# Going East, Longitude increases and going North, Latitude increases.
# For a single point, check if its latitude is greater than the south position and
# less than the northern position. And, check if the longitude is greater than west
# and less than east. These are the limits of a location. If it fails, check the next row
# If it passes, add to the dictionary to have the location as the key, and the MAC addresses
# as values.

# convert the averaged latitude and longitude items to a list.
GPS_avg = []

for key,value in fiDict_avg.items():
	temp = [key, value]
	GPS_avg.append(temp)


# GPS_avg format: [item][Location/GPS][Lat/Long]

MAC_to_place = dict({key : [] for key in location_list})

for item in GPS_avg:

	# extracting Latitude and Longitude coordinates for a given item.
	MAC = item[0]
	Latitude = item[1][0]
	Longitude = item[1][1]

	# search through the Radio Map to see where a MAC address is grouped to!
	for boundary in csv_list:
		
		# allocating for easier to read if statement.
		Location = str(boundary[0])
		North = boundary[1]
		South = boundary[2]
		East = boundary[3]
		West = boundary[4]

		# determine if in confines of pre-defined boundaries.
		if (Latitude >= South[0]) and (Latitude <= North[0]) and (Longitude >= West[1]) and (Longitude <= East[1]):
			MAC_to_place[Location].append(MAC)
			break
		else:
			pass

print(MAC_to_place)




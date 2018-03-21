import numpy as np
import scipy as sp
import csv, os
import collections as cl
import pandas as pd
from functools import partial
import matplotlib.pyplot as plt

error_str = 'Mismatch in Array sizes.'
correct_str = '...Passed Size Test'

# operating on Anaconda Distribution - Python3.6.3 Custom.
script_dir = os.path.dirname(__file__)
csv_path = os.path.join(script_dir, '/CSV/WigleWifi_2018_0220.csv')

with open('CSV/WigleWifi_2018_0220.csv','rt') as f:
	fiReader = csv.reader(f,delimiter=',')
	fiList = list(fiReader)

# panda conversion
df = pd.read_csv('CSV/WigleWifi_2018_0220.csv',delimiter=',',skiprows=0,header=1)

MAC = df.MAC	# pass pertinent data structures to accessible variables.
SSID = df.SSID 						# Access point (Human-readable) network name.
Latitude = df.CurrentLatitude 	# Latitude
Longitude = df.CurrentLongitude 	# Longitude
Channel = df.Channel 				# Channel (Less important)
RSSI = df.RSSI 					 	# Received Signal Strength Integrity.

countMAC = cl.Counter(MAC)		# stores recurring addresses.
countSSID = cl.Counter(SSID)	# store recurring network or access point names.

Time = df.FirstSeen				# imports Time.

uniqueTime = df.FirstSeen.unique()

if(len(Time)!=len(MAC)):
	raise ValueError(error_str)

# MAC, SSID, AuthMode, FirstSeen, Channel, RSSI, Lat, Long, Alt.
elements = fiList[1]		# in case the types per item in fiList are required.
fiList = fiList[2:][:]	# removes meta-data topline and second line of elements.
GPS = []						# pre-allocate.
MAC = []
RSSI = []
results = []

# explicitly accesses the GPS values. [Latitude][Longitude]
for index, value in enumerate(fiList):
	GPS.append(fiList[index][6:8])
	MAC.append(fiList[index][0])
	RSSI.append(fiList[index][5])

GPS = [[float(j) for j in i] for i in GPS]	# converts to float

# creates a dictionary with GPS values mapped to MAC address.
fiDict = dict(zip(MAC,GPS))

MAC_count = cl.Counter(MAC)
RSSI_count = cl.Counter(RSSI)

LatLongDict = dict()


for item in fiDict.items():
	print(str(item) + '\n')

# grabbing avg. Lat/Long
for key,value in fiDict.items():
	if key in LatLongDict.keys():
		print('Caught an instance.')
		LatLongDict[key].append((fiDict[value[0]],fiDict[value[1]]))
	else:
		print('New Key.')
		LatLongDict[str(key)] = (fi)

print(LatLongDict['b4:5d:50:14:26:92'])
#print(fiDict)


def list_duplicates(seq):
    tally = cl.defaultdict(list)
    for i,item in enumerate(seq):
        tally[item].append(i)
    return ((key,locs) for key,locs in tally.items() 
                            if len(locs)>1)

# prints duplicates.
for dup in sorted(list_duplicates(MAC)):
	print(dup)



# MAC Address Histogram.
#plt.bar(range(len(MAC_count)),MAC_count.values(),align="center")
#plt.xticks(range(len(MAC_count)), MAC_count.keys())
#plt.xticks(rotation=70)
#plt.xlabel('MAC Addresses')
#plt.xlim(0, 30)
#plt.ylabel('Frequency')
#plt.show()
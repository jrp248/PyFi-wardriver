import numpy as np
import scipy as sp
import csv, os
import collections as cl
import pandas as pd
from functools import partial

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
results = []

# explicitly accesses the GPS values. [Latitude][Longitude]
for index, value in enumerate(fiList):
	GPS.append(fiList[index][6:8])
	MAC.append(fiList[index][0])

GPS = [[float(j) for j in i] for i in GPS]	# converts to float

# creates a dictionary with GPS values mapped to MAC address.
fiDict = dict(zip(MAC,GPS))

MAC_count = cl.Counter(MAC)


def list_duplicates(seq):
    tally = cl.defaultdict(list)
    for i,item in enumerate(seq):
        tally[item].append(i)
    return ((key,locs) for key,locs in tally.items() 
                            if len(locs)>1)

# prints duplicates.
#for dup in sorted(list_duplicates(MAC)):
#	print(dup)

for key, value in fiDict.items():
	if key == 'b4:5d:50:14:26:90':
		results.append(value)


for key, value in MAC_count.items():
	print(key,value)
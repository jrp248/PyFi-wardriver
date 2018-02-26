import numpy as np
import scipy as sp
import csv, os
import collections as cl
import pandas as pd

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
Latitude = df.CurrentLatitude 		# Latitude
Longitude = df.CurrentLongitude 	# Longitude
Channel = df.Channel 				# Channel (Less important)
RSSI = df.RSSI 					 	# Received Signal Strength Integrity.



countMAC = cl.Counter(MAC)		# stores recurring addresses.
countSSID = cl.Counter(SSID)	# store recurring network or access point names.

Time = df.FirstSeen				# imports Time.

if(len(Time)!=len(MAC)):
	raise ValueError(error_str)

print(df)
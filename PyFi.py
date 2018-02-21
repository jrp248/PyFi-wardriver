import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import csv, os
import collections as cl
import pandas as pd


script_dir = os.path.dirname(__file__)
csv_path = os.path.join(script_dir, '/CSV/WigleWifi_2018_0220.csv')

with open('CSV/WigleWifi_2018_0220.csv','rt') as f:
	fiReader = csv.reader(f,delimiter=',')
	fiList = list(fiReader)


# panda conversion
df = pd.read_csv('CSV/WigleWifi_2018_0220.csv',delimiter=',',skiprows=0,header=1)

MAC = df.MAC	# passes all MAC addresses to a single variable.
SSID = df.SSID

countMAC = cl.Counter(MAC)		# stores recurring addresses.
countSSID = cl.Counter(SSID)	# store recurring network or access point names.

print(countSSID)				# figure out how to gain row indeces from panda dataframes.
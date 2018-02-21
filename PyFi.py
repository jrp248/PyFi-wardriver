import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import csv

# Reading entire file first.

with open('WigleWifi_2018_0220.csv','rt', encoding='utf8') as f:
	fiReader = csv.reader(f, delimiter=',')
	for row in fiReader:
		print(', '.join(row))

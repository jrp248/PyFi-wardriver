import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import csv
import os

script_dir = os.path.dirname(__file__)
csv_path = os.path.join(script_dir, '/CSV/WigleWifi_2018_0220.csv')


with open('CSV/WigleWifi_2018_0220.csv','rt', encoding='utf8') as f:
	fiReader = csv.reader(f, delimiter=',')
	for row in fiReader:
		print(', '.join(row))

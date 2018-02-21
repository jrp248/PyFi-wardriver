import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import csv

with open('WigleWifi_2018_0220.csv','rb') as f:
   reader = csv.reader(f)
   complete = list(reader)
  
print(complete)
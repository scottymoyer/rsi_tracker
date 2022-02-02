import numpy as np
from numpy import genfromtxt

# Read csv into numpy array
linkbtc_data = genfromtxt('linkbtc-rsi-output-100days.csv', delimiter=',', skip_header=1)
linkbtc_rsi_vals = [x[6] for x in linkbtc_data if x[0]>14]
print(linkbtc_rsi_vals)

btclink_data = genfromtxt('btclink-rsi-output-100days.csv', delimiter=',', skip_header=1)
btclink_rsi_vals = [x[6] for x in btclink_data if x[0]>14]
print(btclink_rsi_vals)

signals = []

for i, (l, b) in enumerate(zip(linkbtc_data, btclink_data)):
    if i < 14:
      continue
    if(l[6] > 65 and b[6] < 35):
      signals.append([i, l[6], b[6]])
    elif(l[6] < 35 and b[6] > 65):
      signals.append([i, l[6], b[6]])
print(signals)

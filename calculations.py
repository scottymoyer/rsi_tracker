import numpy as np
from numpy import genfromtxt

def testing():
  # Read csv into numpy array
  linkbtc_data = genfromtxt('csvoutputs/bitcoin-chainlink-rsi-output-2000days.csv', delimiter=',', skip_header=1)
  linkbtc_rsi_vals = [x[6] for x in linkbtc_data[14:]]
  print(linkbtc_rsi_vals)

  btclink_data = genfromtxt('csvoutputs/chainlink-bitcoin-rsi-output-2000days.csv', delimiter=',', skip_header=1)
  btclink_rsi_vals = [x[6] for x in btclink_data[14:]]
  print(btclink_rsi_vals)

  signals = []
  difference = []

  for i, (l, b) in enumerate(zip(linkbtc_data, btclink_data)):
      if i <= 14:
        continue
      if(l[6] > 70 and b[6] < 30):
        signals.append([i, l[6], b[6]])
      elif(l[6] < 30 and b[6] > 70):
        signals.append([i, l[6], b[6]])
      difference.append(l[6]+b[6])
  print(signals)
  for i in difference:
    if (i > 102 or i < 98):
      print(i)
  return
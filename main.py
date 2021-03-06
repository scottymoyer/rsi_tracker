import numpy as np
from numpy import genfromtxt
import pandas as pd
import csv
from pycoingecko import CoinGeckoAPI
cg = CoinGeckoAPI()

#Set number of days and (T/F) for log scale 
numdays = 50

#Set token ids
xcoinid = 'chainlink'

#Get token data
xcoin = cg.get_coin_market_chart_by_id(id=xcoinid, vs_currency='usd', days=numdays, interval='daily')


#Put prices for token into lists
xvals = [xcoin['prices'][i][1] for i in range(len(xcoin['prices']))]


print(xvals)


wilder_prices = xvals

# Define window length and window
window_length = 14
window = []

# Initialize avg gain and loss arrays
gains = []
losses = []

prev_avg_gain = None
prev_avg_loss = None

# Create a container for our final output (as a csv)
output = [['date', 'close', 'gain', 'loss', 'avg_gain', 'avg_loss', 'rsi']]

# Enumerate wilder prices to calculate rsi
for i, price in enumerate(wilder_prices):
  if i == 0:
    window.append(price)
    output.append([i+1, price, 0, 0, 0, 0, 0])
    continue

  # Calculate difference between periods
  difference = wilder_prices[i] - wilder_prices[i-1]

  if difference > 0:
    gain = difference
    loss = 0

  elif difference < 0:
    loss = abs(difference)
    gain = 0

  else:
    gain = 0
    loss = 0

  # Save gains/losses
  gains.append(gain)
  losses.append(loss)
  
  # Continue to iterate until you reach the window length in order to calculate initial RSI value
  if i < window_length:
    window.append(price)
    output.append([i+1, price, gain, loss, 0, 0, 0])
    continue

  # SMA for first avg gain
  if i == window_length:
    avg_gain = sum(gains) / window_length
    avg_loss = sum(losses) / window_length

  # WMA
  else:
    avg_gain = (prev_avg_gain * (window_length - 1) + gain) / window_length
    avg_loss = (prev_avg_loss * (window_length - 1) + loss) / window_length

  # Keep in memory
  prev_avg_gain = avg_gain
  prev_avg_loss = avg_loss

  # Calculate RS
  rs = avg_gain / avg_loss

  # Calculate RSI
  rsi = 100 - (100 / (1 + rs))

  # Remove oldest values
  window.append(price)
  window.pop(0)
  gains.pop(0)
  losses.pop(0)

  # Save Data
  output.append([i+1, price, round(gain, 2), round(loss, 2), round(avg_gain, 2), round(avg_loss, 2), round(rsi, 2)])

print(output)

# Create a new CSV file to store output data
with open('wilder-rsi-output.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(output)




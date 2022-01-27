import numpy as np
from numpy import genfromtxt
import pandas as pd
import csv
from pycoingecko import CoinGeckoAPI
cg = CoinGeckoAPI()

#Set number of days and (T/F) for log scale 
numdays = 14

#Set token ids
xcoinid = 'chainlink'

#Get token data
xcoin = cg.get_coin_market_chart_by_id(id=xcoinid, vs_currency='usd', days=numdays, interval='daily')


#Put prices for tokens into lists
xvals = [xcoin['prices'][i][1] for i in range(len(xcoin['prices']))]


print(xvals)


# Read csv into numpy array
wilder_data = genfromtxt('wilder-rsi-data.csv', delimiter=',', skip_header=1)
wilder_prices = [x[1] for x in wilder_data]

# View the Data
print(wilder_prices)

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

'''
print('New case')
# Load the data via Python's CSV module
with open('wilder-rsi-data.csv', 'r')as file:
    reader = csv.reader(file)
    header = next(reader)  # skip the header
    readerlist = list(reader)
    wilder_data = [float(row[1]) for row in readerlist]
# View the Data
print(wilder_data)

# Define our Lookback period (our sliding window)
window_length = 14

# Initialize containers for avg. gains and losses
gains = []
losses = []

# Create a container for current lookback prices
window = []

# Keeps track of previous average values
prev_avg_gain = None
prev_avg_loss = None

# Create a container for our final output (as a csv)
output = [['date', 'close', 'gain', 'loss', 'avg_gain', 'avg_loss', 'rsi']]

# Loop through an enumerated set of our data
# to keep track of which period we are currently
# making calculations for.
for i, price in enumerate(wilder_data):
  # keep track of the price for the first period
  # but don't calculate a difference value.
  if(i==0):
    window.append(price)
    output.append([i+1,price,0,0,0,0,0])
    continue
  # After the first period, calculate the difference
  # between price and previous price as a rounded value
  difference = round(wilder_data[i]-wilder_data[i-1], 2)

  # Record positive differences as gains
  if difference > 0:
      gain = difference
      loss = 0
  # Record negative differences as losses
  elif difference < 0:
      gain = 0
      loss = abs(difference)
  # Record no movements as neutral
  else:
      gain = 0
      loss = 0

  # Save gains/losses
  gains.append(gain)
  losses.append(loss)

  # Continue to iterate until enough
  # gains/losses data is available to 
  # calculate the initial RS value
  if i < window_length:
      window.append(price)
      output.append([i+1, price, gain, loss, 0, 0, 0])
      continue

  # Calculate SMA for first gain
  if i == window_length:
      avg_gain = sum(gains) / len(gains)
      avg_loss = sum(losses) / len(losses)

  # Use WSM after initial window-length period
  else:
      avg_gain = (prev_avg_gain * (window_length - 1) + gain) / window_length
      avg_loss = (prev_avg_loss * (window_length - 1) + loss) / window_length

  # Keep in memory
  prev_avg_gain = avg_gain
  prev_avg_loss = avg_loss

  # Round for later comparison (optional)
  avg_gain = round(avg_gain, 2)
  avg_loss = round(avg_loss, 2)
  prev_avg_gain = round(prev_avg_gain, 2)
  prev_avg_loss = round(prev_avg_loss, 2)

  # use avg. gains and losses to calculate
  # the RS value rounded to the nearest 
  # 2 decimal places
  rs = round(avg_gain / avg_loss, 2)

  # use the RS value to calculate the 
  # RSI to the nearest 2 decimal places
  rsi = round(100 - (100 / (1 + rs)), 2)

  # Remove oldest values
  window.append(price)
  window.pop(0)
  gains.pop(0)
  losses.pop(0)

  # Save Data
  output.append([i+1, price, gain, loss, avg_gain, avg_loss, rsi])



print(window)
print(output)

# Create a new CSV file to store output data
with open('wilder-rsi-output.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(output)


#Set number of days and (T/F) for log scale 
numdays = 14
logscale = True

#Set token ids
xcoinid = 'gmx'
ycoinid = 'oasis-network'

#Get token data
xcoin = cg.get_coin_market_chart_by_id(id=xcoinid, vs_currency='usd', days=numdays, interval='daily')

ycoin = cg.get_coin_market_chart_by_id(id=ycoinid, vs_currency='usd', days=numdays, interval='daily')

#Put prices for tokens into lists
xvals = [xcoin['prices'][i][1] for i in range(len(xcoin['prices']))]

yvals = [ycoin['prices'][i][1] for i in range(len(ycoin['prices']))]

print(xvals)
print(yvals)
'''


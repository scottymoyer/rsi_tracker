import numpy as np
from numpy import genfromtxt
import pandas as pd
import csv
from pycoingecko import CoinGeckoAPI
cg = CoinGeckoAPI()



# Read csv into numpy array
wilder_data = genfromtxt('wilder-rsi-data.csv', delimiter=',')

# View the Data
print(wilder_data)


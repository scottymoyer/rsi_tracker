import numpy as np
from numpy import genfromtxt
import pandas as pd
import csv
from pycoingecko import CoinGeckoAPI
cg = CoinGeckoAPI()

class PriceBasket:

  def __init__(self, tokens, ccy='usd', start_date=0, end_date=0):
    if type(self.tokens)==str:
      self.tokens = (self.tokens,)
    self.tokens = tokens
    self.currency = ccy
    self.start_date = start_date
    self.end_date = end_date
    self.interval = 'daily'
    """
    self.numdays = int(convertToDays(self.end_date) - convertToDays(self.start_date))

    self.token_basket = (self.currency,) + tuple(self.tokens)
    self.numtokens = len(self.token_basket)
    """

  def createTokenBasket(self):
    # Handle single token value
    if type(self.tokens)==str:
      self.tokens = (self.tokens,)
    self.token_basket = (self.currency,) + tuple(self.tokens)
    self.numtokens = len(self.token_basket)
    return self.token_basket

  def returnTokenNum(self, token):
    return self.token_basket.index(token)

  def calculateNumdays(self):
    self.numdays = 100
    pass
    """
    self.numdays = int(convertToDays(self.end_date) - convertToDays(self.start_date))
    """


  def createPriceBasket(self):
    self.price_basket = np.ndarray(shape=(self.numdays,self.numtokens,self.numtokens))

  def loadTokenPrice(self, token):
    # Set token num
    tokenNum = self.token_basket.index(token)

    #Get token data
    token_data = cg.get_coin_market_chart_by_id(id=token, vs_currency=self.currency, days=self.numdays, interval=self.interval)

    #Put prices for token into Price Basket
    for i, x in enumerate(token_data['prices'][::-1][1]):
      self.price_basket[i][0][tokenNum] = x

  def loadAllTokenPrices(self):
    for t in self.tokens:
      self.loadTokenPrice(t)

  def calculateRelativeTokenPrices(self):
    
      



    

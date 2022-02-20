from collections import defaultdict
from email.policy import default
from email.quoprimime import quote
from logging import raiseExceptions
from multiprocessing.sharedctypes import Value
import os
import datetime
from pickle import NONE
from queue import Empty
import pandas as pd
from ticker import *
from traderbot import *
from strategy import *
from market import *
import matplotlib.pyplot as plt


class Trader():
    def __init__(self, strategy, stocks, commodities, aggressiveness=1.01, cash=100000):
        self.market = Market(stocks, commodities)

        self.startDate = self.market.startDate
        self.endDate = self.market.endDate
        self.date = self.market.startDate
        self.account = TraderBot(self.startDate, cash)


        if (strategy == 'Leveraged Pair'):
            self.strategy = Leveraged_Strategy(stocks[0], stocks[1], 3, aggressiveness)
        else:
            self.strategy = None
    
    def action(self):
        while (self.date <= self.endDate):
            quotes = self.market.getMarket(self.date)
            # print(quotes)
            if (quotes != None):
                if (self.strategy.name == 'Leveraged Pair'):
                    stockAPrice = quotes[self.strategy.stockA]
                    stockBPrice = quotes[self.strategy.stockB]
                    AClose = float(stockAPrice['Close'])
                    BClose = float(stockBPrice['Close'])
                
                    allocation = self.strategy.update(AClose, BClose)

                    ashares = int(allocation * BClose - self.account.position[self.strategy.stockA])
                    bshares = int(-allocation * AClose * self.strategy.ratio - self.account.position[self.strategy.stockB])
                    
                    if (ashares > 0):
                        self.account.sell(self.strategy.stockB, BClose, abs(bshares))
                        self.account.buy(self.strategy.stockA, AClose, ashares)
                    elif (ashares < 0):
                        self.account.sell(self.strategy.stockA, AClose, abs(ashares))
                        self.account.buy(self.strategy.stockB, BClose, bshares)

                    self.account.calculate_value(quotes)
                    print(self.account.cash)
            self.date = addDate(self.date)
       
        
def main():
    me = Trader('Leveraged Pair', ['UPRO', 'SPY'], [])
    me.action()
    # for key in me.account.tradelog.keys():
    #     for i in range(len(me.account.tradelog[key])):
    #         print(me.account.tradelog[key][i])
    print(me.account.position)
    me.account.accountvalue.plot(x='Date', y='Net Value')
    plt.show()
if __name__ == '__main__':
    main()
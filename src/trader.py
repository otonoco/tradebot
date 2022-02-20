from collections import defaultdict
from logging import raiseExceptions
import os
import datetime
import pandas as pd
from ticker import *
from traderbot import *
from strategy import *
from market import *
import matplotlib.pyplot as plt


class Trader():
    def __init__(self, strategy, stocks, commodities, aggressiveness=0.0001, cash=1000000, factor=10000):
        self.market = Market(stocks, commodities)

        self.startDate = self.market.startDate
        self.endDate = self.market.endDate
        self.date = self.market.startDate
        self.account = TraderBot(self.startDate, cash)

        if (strategy == 'Leveraged Pair'):
            self.strategy = Leveraged_Strategy(stocks[0], stocks[1], 3, aggressiveness, factor)
        else:
            self.strategy = None
    
    
    def action(self):
        last_allocation = 0
        while (self.date <= self.endDate):
            quotes = self.market.getMarket(self.date)
            if (quotes != None):
                if (self.strategy.name == 'Leveraged Pair'):
                    stockAPrice = quotes[self.strategy.stockA]
                    stockBPrice = quotes[self.strategy.stockB]
                    AClose = float(stockAPrice['Close'])
                    BClose = float(stockBPrice['Close'])
                    AVolume = int(stockAPrice['Volume'])
                    BVolume = int(stockBPrice['Volume'])
                
                    allocation = self.strategy.update(AClose, BClose)
                    if (last_allocation != allocation):
                        ashares = int(allocation * BClose - self.account.position[self.strategy.stockA])
                        bshares = int(-allocation * AClose * self.strategy.ratio - self.account.position[self.strategy.stockB])
                        if (ashares > 0):
                            self.account.buy(self.strategy.stockA, AClose, ashares, AVolume)

                            need = int((-(self.account.position[self.strategy.stockA]) * AClose * self.strategy.ratio) / BClose - self.account.position[self.strategy.stockB])
                            self.account.sell(self.strategy.stockB, BClose, min(abs(need), BVolume))
                            
                        elif (ashares < 0):
                            self.account.buy(self.strategy.stockB, BClose, bshares, BVolume)
                            
                            need = int(-(self.account.position[self.strategy.stockB] * BClose) / (AClose * self.strategy.ratio) - self.account.position[self.strategy.stockA])
                            self.account.sell(self.strategy.stockA, AClose, min(abs(need), AVolume))
                            
                    last_allocation = allocation
                    self.account.calculate_value(quotes)
                    print(self.account.cash)
            self.date = addDate(self.date)
       
        
def main():
    me = Trader('Leveraged Pair', ['UPRO', 'SPY'], [])
    me.action()
    print(me.account.position)
    me.account.accountvalue.plot(x='Date', y='Net Value')
    plt.show()


if __name__ == '__main__':
    main()
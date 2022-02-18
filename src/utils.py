from collections import defaultdict
from logging import raiseExceptions
from multiprocessing.sharedctypes import Value
import os
import datetime
from queue import Empty
import pandas as pd


def dictMerge(dict1, dict2):
    return {**dict1, **dict2}


def addDate(date):
    return date + datetime.timedelta(1)


## The Stock Data Object
class Stock():
    def __init__(self, ticker):
        self.name = ticker
        self.data = self.rename(ticker)

    def rename(self, ticker):
        path = '../quantoa/ml/archive/individual_stocks_5yr/individual_stocks_5yr/' + ticker + '_data.csv'
        try:
            file = pd.read_csv(path)
            file.dropna()
            if ('date' in file.columns):
                file = file.rename(columns={'date' : 'Date'})
            if ('open' in file.columns):
                file = file.rename(columns={'open' : 'Open'})
            if ('close' in file.columns):
                file = file.rename(columns={'close' : 'Close'})
            if ('high' in file.columns):
                file = file.rename(columns={'high' : 'High'})
            if ('low' in file.columns):
                file = file.rename(columns={'low' : 'Low'})
            if ('volume' in file.columns):
                file = file.rename(columns={'volume' : 'Volume'})
            
            return file
        except ValueError:
            print('no ticker found')
        

## The Commodity Data Object
class Commodity():
    def __init__(self, ticker):
        self.name = ticker
        self.data = self.readData(ticker)

    def readData(self, ticker):
        path = '../quantoa/ml/Commodity Data/' + ticker + '.csv'
        try:
            file = pd.read_csv(path)
            file.dropna()
            if ('date' in file.columns):
                file = file.rename(columns={'date' : 'Date'})
            if ('open' in file.columns):
                file = file.rename(columns={'open' : 'Open'})
            if ('close' in file.columns):
                file = file.rename(columns={'close' : 'Close'})
            if ('high' in file.columns):
                file = file.rename(columns={'high' : 'High'})
            if ('low' in file.columns):
                file = file.rename(columns={'low' : 'Low'})
            if ('volume' in file.columns):
                file = file.rename(columns={'volume' : 'Volume'})
            
            return file
        except ValueError:
            print('no ticker found')
        
    

class TraderBot():
    def __init__(self, startDate, endDate, strategy, aggressiveness, tickers, cash=1000000):
        ## Inital values
        self.startDate = startDate
        self.endDate = endDate
        self.strat = strategy
        self.aggressiveness = aggressiveness
        self.cash = cash
        self.tickers = tickers

        ## Self Values
        self.position = defaultdict(int)
        self.pnl = 0
        self.pnlPerTicker = defaultdict(int)
        self.tradelog = defaultdict(list)

    
    def buy(self, ticker, price, amount):
        if ((price * amount < self.cash) and (self.riskAnalysis(ticker, price, amount))):
            self.cash -= int(price * amount)
            self.position[ticker] += amount
            self.tradelog[ticker].append('Buy ' + ticker + ' at ' + price + ' for ' + amount)


    def sell(self, ticker, price, amount):
        if (self.position[ticker] > amount):
            self.position[ticker] -= amount
            self.cash += price * amount
            self.tradelog[ticker].append('Sell ' + ticker + ' at ' + price + ' for ' + amount)
        else:
            if (self.riskAnalysis(ticker, price, amount)):
                self.position[ticker] -= amount
                self.cash += price * amount
                self.tradelog[ticker].append('Sell ' + ticker + ' at ' + price + ' for ' + amount)
    

    def riskAnalysis(self, ticker, price, amount):
        if (abs(self.position[ticker] + amount) * price >= 0.5 * self.cash):
            return False
        return True


class Market():
    def __init__(self, stocks, commodities):
        self.tradables = self.filter(stocks, commodities)


    def getQuote(self, ticker, date):
        if ((date < self.startDate) or (date > self.endDate) or (ticker not in self.tradables)):
            raise ValueError
        dateinstring = str(date)[ : 10]
        if (self.tradables[ticker].loc[self.tradables[ticker]['Date'] == dateinstring].empty):
            return None
        return self.tradables[ticker].loc[self.tradables[ticker]['Date'] == dateinstring]

    def getMarket(self, date):
        marketData = defaultdict(pd.DataFrame)
        for ticker in self.tradables.keys():
            marketData[ticker] = self.getQuote(ticker, date)
        return marketData


    def filter(self, stocks, commodities):
        all = stocks + commodities
        start_dates = []
        end_dates = []
        for ticker in all:
            name = ticker.name
            data = ticker.data
            if ('date' in data):
                start_dates.append(min(data['date']))
                end_dates.append(max(data['date']))
            elif ('Date' in data):
                start_dates.append(min(data['Date']))
                end_dates.append(max(data['Date']))
            else:
                raise Exception('No time found in seires')
        start_date = max(start_dates)
        end_date = min(end_dates)
        self.startDate = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        self.endDate = datetime.datetime.strptime(end_date, "%Y-%m-%d")
        filtered = defaultdict(pd.DataFrame)

        for ticker in all:
            name = ticker.name
            data = ticker.data
            if ('date' in data):
                cond1 = data['date'] >= start_date
                cond2 = data['date'] <= end_date
                filtered[name] = data[cond1 & cond2].reset_index(drop=True)
                filtered[name].dropna()
            elif ('Date' in data):
                cond1 = data['Date'] >= start_date
                cond2 = data['Date'] <= end_date
                filtered[name] = data[cond1 & cond2].reset_index(drop=True)
                filtered[name].dropna()

            else:
                raise Exception('No time found in seires')

        return filtered



class MA():
    def __init__(self, tickers, timerange=[5, 30, 60]):
        self.stats = defaultdict(list)
        self.tickers = tickers
        self.short = timerange[0]
        self.midle = timerange[1]
        self.longr = timerange[2]

    def update(self, ticker):
        if (ticker not in self.tickers):
            raise Exception('no data found')
        if (len(self.stats[ticker]) < 60):
            
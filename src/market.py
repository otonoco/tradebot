from collections import defaultdict
import pandas as pd
import datetime
from utils import *
from ticker import *


class Market():
    def __init__(self, stocks, commodities):
        self.stockData = defaultdict(pd.DataFrame)
        self.commodityData = defaultdict(pd.DataFrame)
        for stock in stocks:
            self.stockData[stock] = Stock(stock)
        for commodity in commodities:
            self.commodityData[commodity] = Commodity(commodity)

        self.tradables = self.filter(self.stockData, self.commodityData)


    def getQuote(self, ticker, date):
        if ((date < self.startDate) or (date > self.endDate) or (ticker not in self.tradables)):
            raise ValueError
        dateinstring = str(date)[ : 10]
        if (self.tradables[ticker].loc[self.tradables[ticker]['Date'] == dateinstring].empty):
            return None, False
        return self.tradables[ticker].loc[self.tradables[ticker]['Date'] == dateinstring], True

    def getMarket(self, date):
        marketData = defaultdict(pd.DataFrame)
        for ticker in self.tradables.keys():
            marketData[ticker], valid = self.getQuote(ticker, date)
            if (not valid):
                return None
        return marketData


    def filter(self, stocks, commodities):
        all = dictMerge(stocks, commodities)
        start_dates = []
        end_dates = []
        for ticker in all.keys():
            data = all[ticker].data
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

        for ticker in all.keys():
            data = all[ticker].data
            if ('date' in data):
                cond1 = data['date'] >= start_date
                cond2 = data['date'] <= end_date
                filtered[ticker] = data[cond1 & cond2].reset_index(drop=True)
                filtered[ticker].dropna()
            elif ('Date' in data):
                cond1 = data['Date'] >= start_date
                cond2 = data['Date'] <= end_date
                filtered[ticker] = data[cond1 & cond2].reset_index(drop=True)
                filtered[ticker].dropna()

            else:
                raise Exception('No time found in seires')

        return filtered


def main():
    nyse = Market(['AAPL', 'AMZN'], ['Crude Oil', 'Natural Gas'])
    print(nyse.startDate)

    print(nyse.getQuote('AAPL', nyse.startDate + datetime.timedelta(5)))

if __name__ == '__main__':
    main()
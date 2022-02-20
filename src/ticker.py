from unicodedata import name
import pandas as pd

## The Stock Data Object
class Stock():
    def __init__(self, ticker):
        self.name = ticker
        self.data = self.rename(ticker)

    def rename(self, ticker):
        path = '../../quantoa/ml/archive/individual_stocks_5yr/individual_stocks_5yr/' + ticker + '_data.csv'
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
        path = '../../quantoa/ml/Commodity Data/' + ticker + '.csv'
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


def main():
    apple = Stock('AAPL')
    crudeoil = Commodity('Crude Oil')
    print(apple.data)
    print(crudeoil.data)

if __name__ == '__main__':
    main()
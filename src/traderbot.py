from collections import defaultdict
from operator import index
import pandas as pd

class TraderBot():
    def __init__(self, start_date, cash=1000000):
        ## Inital values
        self.cash = cash

        ## Self Values
        self.position = defaultdict(int)
        self.pnl = 0
        self.pnlPerTicker = defaultdict(int)
        self.tradelog = defaultdict(list)
        self.accountvalue = pd.DataFrame(data={'Date' : [start_date], 'Net Value' : [self.cash]})
        self.value = self.cash


    def calculate_value(self, quotes):
        values = self.cash
        for stock in self.position.keys():
            date = quotes[stock]['Date']
            values += self.position[stock] * float(quotes[stock]['Close'])
        self.value = values
        newdata = pd.DataFrame(data={'Date' : [date], 'Net Value' : [self.value]})
        self.accountvalue = pd.concat([self.accountvalue, newdata], ignore_index=True)
        self.accountvalue.reset_index()
    

    def buy(self, ticker, price, amount):
        self.cash -= price * amount
        self.position[ticker] += amount
        self.tradelog[ticker].append('Buy ' + ticker + ' at ' + str(price) + ' for ' + str(amount))


    def sell(self, ticker, price, amount):
        self.cash += price * amount
        self.position[ticker] -= amount
        self.tradelog[ticker].append('Sell ' + ticker + ' at ' + str(price) + ' for ' + str(amount))


    def riskAnalysis(self, ticker, price, amount):
        ## Reject the trade if the net position after trading will be more than half of the account value
        if (abs(self.position[ticker] + amount) * price >= 0.5 * self.value):
            return False
        return True


def main():
    bot = TraderBot('2020-01-01')
    print(bot.accountvalue)

    bot.buy('AMZN', 3000, 700)
    print(bot.position, bot.cash)
    bot.sell('AMZN', 3500, 700)
    print(bot.position, bot.cash)
    print(bot.tradelog)
if __name__ == '__main__':
    main()
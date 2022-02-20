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
        self.accountvalue = pd.DataFrame(data={'Date' : [start_date], 'Value' : [self.cash]})
        self.value = self.cash


    def calculate_value(self, quotes):
        values = self.cash
        for stock in self.position.keys():
            date = quotes[stock]['Date']
            values += self.position[stock] * float(quotes[stock]['Close'])
        self.value = values
        newdata = pd.DataFrame(data={'Date' : [date], 'Value' : [self.value]})
        self.accountvalue = pd.concat([self.accountvalue, newdata], ignore_index=True)
        self.accountvalue.reset_index()
    

    def buy(self, ticker, price, amount):
        self.cash -= price * amount
        self.position[ticker] += amount
        self.tradelog[ticker].append('Buy ' + ticker + ' at ' + str(price) + ' for ' + str(amount))
        # if ((price * amount < self.cash) and (self.riskAnalysis(ticker, price, amount))):
        #     self.cash -= price * amount
        #     self.position[ticker] += amount
        #     self.tradelog[ticker].append('Buy ' + ticker + ' at ' + str(price) + ' for ' + str(amount))
        # else:
        #     if (self.position[ticker] >= 0):
        #         cash_possible = int(self.cash // price)
        #         risk_possible = int((0.5 * self.value - abs(price * self.position[ticker])) // price)
        #         amount = min(cash_possible, risk_possible)
        #         self.cash -= price * amount
        #         self.position[ticker] += amount
        #         self.tradelog[ticker].append('Buy ' + ticker + ' at ' + str(price) + ' for ' + str(amount))
        #     else:
        #         cash_possible = int(self.cash // price)
        #         risk_possible = int(0.5 * self.value // price)
        #         amount = min(cash_possible, abs(self.position[ticker]) + risk_possible)
        #         self.cash -= price * amount
        #         self.position[ticker] += amount
        #         self.tradelog[ticker].append('Buy ' + ticker + ' at ' + str(price) + ' for ' + str(amount))


    def sell(self, ticker, price, amount):
        self.cash += price * amount
        self.position[ticker] -= amount
        self.tradelog[ticker].append('Sell ' + ticker + ' at ' + str(price) + ' for ' + str(amount))
        ## Case 1: Sell our long position, and remaining long after trade 
        # if (self.position[ticker] >= amount):
        #     self.cash += price * amount
        #     self.position[ticker] -= amount
        #     self.tradelog[ticker].append('Sell ' + ticker + ' at ' + str(price) + ' for ' + str(amount))
        # else:
        #     ## We will be short after the trade
        #     ## Do risk check
            
        #     if (self.position[ticker] < 0):
        #         if (self.riskAnalysis(ticker, price, -amount)):
        #             self.cash += price * amount
        #             self.position[ticker] -= amount
        #             self.tradelog[ticker].append('Sell ' + ticker + ' at ' + str(price) + ' for ' + str(amount))
        #         else:
        #             risk_possible = int((0.5 * self.value - abs(self.position[ticker] * price)) // price)
        #             self.cash += price * risk_possible
        #             self.position[ticker] -= risk_possible
        #             self.tradelog[ticker].append('Sell ' + ticker + ' at ' + str(price) + ' for ' + str(risk_possible))
        #     else:
        #         risk_possible = int(0.5 * self.value // price)
        #         real_amount = min(risk_possible + self.position[ticker], amount)
        #         self.cash += price * real_amount
        #         self.position[ticker] -= real_amount
        #         self.tradelog[ticker].append('Sell ' + ticker + ' at ' + str(price) + ' for ' + str(real_amount))


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
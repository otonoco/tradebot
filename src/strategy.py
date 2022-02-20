class Leveraged_Strategy():
    def __init__(self, tickerA, tickerB, leveragedRatio, threshhold):
        self.stockA = tickerA
        self.stockB = tickerB
        self.ratio = leveragedRatio
        self.threshold = threshhold
        self.lastA = 0
        self.lastB = 0
        self.allocation = 0
        self.name = 'Leveraged Pair'
        

    def update(self, stock_a_price, stock_b_price):
        if ((self.lastA == 0) or self.lastB == 0):
            self.lastA = stock_a_price
            self.lastB = stock_b_price
            return 0
        else:
            self.allocation = self.calculate(stock_a_price, stock_b_price)
            self.lastA = stock_a_price
            self.lastB = stock_b_price
            return self.allocation
    

    def calculate(self, stock_a_today, stock_b_today):
        stock_a_change = (stock_a_today / self.lastA) - 1
        stock_b_change = (stock_b_today / self.lastB) - 1
        if (stock_a_change > self.threshold * self.ratio * stock_b_change):
            allocation = -30
        elif (stock_a_change < -self.threshold * self.ratio * stock_b_change):
            allocation = 30
        else:
            allocation = 0
        
        return allocation
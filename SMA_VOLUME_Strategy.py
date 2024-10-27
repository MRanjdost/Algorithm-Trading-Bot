from backtesting import Backtest, Strategy
from backtesting.lib import crossover
import talib as tb
import pandas as pd

class SMA_Volume_Strategy(Strategy):
    def init(self):
        close = self.data.Close.astype(float)
        volume = self.data.Volume.astype(float)
        
        self.sma_short = self.I(tb.SMA, close, 5)
        self.sma_long = self.I(tb.SMA, close, 20)
        
        self.avg_volume = self.I(lambda x: pd.Series(x).rolling(window=20).mean(), volume)

    def next(self):
        price = self.data.Close[-1]
        volume = self.data.Volume[-1]
        
        stop_loss_long = price - (price * 0.03)
        take_profit_long = price + 1.5 * (price - stop_loss_long)
        
        stop_loss_short = price + (price * 0.03)
        take_profit_short = price - 1.5 * (stop_loss_short - price)
        
        if crossover(self.sma_short, self.sma_long) and volume > self.avg_volume[-1]:
            self.buy(sl=stop_loss_long, tp=take_profit_long)
        
        elif crossover(self.sma_long, self.sma_short) and volume > self.avg_volume[-1]:
            self.sell(sl=stop_loss_short, tp=take_profit_short)



data = pd.read_csv(r"E:\idea youtube\algoTrading\btc_usd_data.csv", parse_dates=['Datetime'], index_col='Datetime')
data.columns = [column.capitalize() for column in data.columns]
data = data.dropna()

bt = Backtest(data, SMA_Volume_Strategy, cash=1000000, commission=0.002)

result = bt.run()

bt.plot()

print(result)

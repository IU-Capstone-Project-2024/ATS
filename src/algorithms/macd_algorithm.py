import pandas as pd
import matplotlib.pyplot as plt
from .algorithm import Algorithm

class MACDAlgorithm(Algorithm):
    def __init__(self, symbol: str, data: pd.DataFrame, short_window: int, long_window: int, signal_window: int):
        super().__init__(symbol, data)
        self.short_window = short_window
        self.long_window = long_window
        self.signal_window = signal_window

    def generate_signals(self):
        self.signals['MACD'] = self.data['close'].ewm(span=self.short_window, adjust=False).mean() - \
                               self.data['close'].ewm(span=self.long_window, adjust=False).mean()
        self.signals['Signal'] = self.signals['MACD'].ewm(span=self.signal_window, adjust=False).mean()
        self.signals['Hist'] = self.signals['MACD'] - self.signals['Signal']
        self.signals['price'] = self.data['close']
        self.signals['signal'] = 0.0
        self.signals.loc[self.signals['MACD'] > self.signals['Signal'], ['signal']] = 1.0
        self.signals.loc[self.signals['MACD'] < self.signals['Signal'], ['signal']] = -1.0


    def plot_signals(self, n_intervals=100):
        plt.figure(figsize=(14, 7))
        plt.plot(self.data['close'][-n_intervals:], label='Close Price')
        macd_signals = self.signals[-n_intervals:]
        plt.plot(macd_signals[macd_signals['signal'] == 1.0].index,
                 macd_signals['price'][macd_signals['signal'] == 1.0],
                 '^', markersize=10, color='m', label='Buy Signal')
        plt.plot(macd_signals[macd_signals['signal'] == -1.0].index,
                 macd_signals['price'][macd_signals['signal'] == -1.0],
                 'v', markersize=10, color='k', label='Sell Signal')
        """plt.plot(macd_signals['Signal'], label='Signal Line')
        plt.bar(macd_signals.index, macd_signals['Hist'], label='Histogram')
        plt.title(f'{self.symbol} - MACD Strategy')"""
        plt.legend()
        plt.show()

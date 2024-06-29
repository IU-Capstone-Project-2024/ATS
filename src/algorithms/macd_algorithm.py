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
        self.signals['MACD'] = self.data['Close'].ewm(span=self.short_window, adjust=False).mean() - \
                               self.data['Close'].ewm(span=self.long_window, adjust=False).mean()
        self.signals['Signal'] = self.signals['MACD'].ewm(span=self.signal_window, adjust=False).mean()
        self.signals['Hist'] = self.signals['MACD'] - self.signals['Signal']
        self.signals['signal'] = 0.0
        self.signals['signal'][self.signals['MACD'] > self.signals['Signal']] = 1.0
        self.signals['signal'][self.signals['MACD'] < self.signals['Signal']] = -1.0

    def plot_signals(self):
        plt.figure(figsize=(14, 7))
        plt.plot(self.data['Close'], label='Close Price')
        plt.plot(self.signals['MACD'], label='MACD')
        plt.plot(self.signals['Signal'], label='Signal Line')
        plt.bar(self.signals.index, self.signals['Hist'], label='Histogram')
        plt.title(f'{self.symbol} - MACD Strategy')
        plt.legend()
        plt.show()

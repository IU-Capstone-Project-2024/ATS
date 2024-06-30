import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from .algorithm import Algorithm

class SMAAlgorithm(Algorithm):
    def __init__(self, symbol: str, data: pd.DataFrame, short_window: int, long_window: int):
        super().__init__(symbol, data)
        self.short_window = short_window
        self.long_window = long_window

    def generate_signals(self):
        self.signals['short_mavg'] = self.data['close'].rolling(window=self.short_window, min_periods=1).mean()
        self.signals['long_mavg'] = self.data['close'].rolling(window=self.long_window, min_periods=1).mean()
        self.signals['signal'] = 0.0
        self.signals['signal'][self.short_window:] = \
            np.where(self.signals['short_mavg'][self.short_window:] > self.signals['long_mavg'][self.short_window:], 1.0, 0.0)
        self.signals['positions'] = self.signals['signal'].diff()

    def plot_signals(self):
        plt.figure(figsize=(14, 7))
        plt.plot(self.data['Close'], label='Close Price')
        plt.plot(self.signals['short_mavg'], label='Short Moving Average')
        plt.plot(self.signals['long_mavg'], label='Long Moving Average')
        plt.plot(self.signals[self.signals['positions'] == 1.0].index,
                 self.signals['short_mavg'][self.signals['positions'] == 1.0],
                 '^', markersize=10, color='m', label='Buy Signal')
        plt.plot(self.signals[self.signals['positions'] == -1.0].index,
                 self.signals['short_mavg'][self.signals['positions'] == -1.0],
                 'v', markersize=10, color='k', label='Sell Signal')
        plt.title(f'{self.symbol} - SMA Strategy')
        plt.legend()
        plt.show()

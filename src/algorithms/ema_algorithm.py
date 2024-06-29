import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from .algorithm import Algorithm

class EMAAlgorithm(Algorithm):
    def __init__(self, symbol: str, data: pd.DataFrame, short_window: int, long_window: int):
        super().__init__(symbol, data)
        self.short_window = short_window
        self.long_window = long_window

    def generate_signals(self):
        self.signals['short_ema'] = self.data['Close'].ewm(span=self.short_window, adjust=False).mean()
        self.signals['long_ema'] = self.data['Close'].ewm(span=self.long_window, adjust=False).mean()
        self.signals['signal'] = 0.0
        self.signals['signal'][self.short_window:] = \
            np.where(self.signals['short_ema'][self.short_window:] > self.signals['long_ema'][self.short_window:], 1.0, 0.0)
        self.signals['positions'] = self.signals['signal'].diff()

    def backtest(self):
        # Реализация метода бэктестинга для EMA
        pass

    def plot_signals(self):
        plt.figure(figsize=(14, 7))
        plt.plot(self.data['Close'], label='Close Price')
        plt.plot(self.signals['short_ema'], label='Short EMA')
        plt.plot(self.signals['long_ema'], label='Long EMA')
        plt.plot(self.signals[self.signals['positions'] == 1.0].index,
                 self.signals['short_ema'][self.signals['positions'] == 1.0],
                 '^', markersize=10, color='m', label='Buy Signal')
        plt.plot(self.signals[self.signals['positions'] == -1.0].index,
                 self.signals['short_ema'][self.signals['positions'] == -1.0],
                 'v', markersize=10, color='k', label='Sell Signal')
        plt.title(f'{self.symbol} - EMA Strategy')
        plt.legend()
        plt.show()

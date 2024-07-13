import pandas as pd
import matplotlib.pyplot as plt
from .algorithm import Algorithm

class BollingerBandsAlgorithm(Algorithm):
    def __init__(self, symbol: str, data: pd.DataFrame, window: int, num_std_dev: int):
        super().__init__(symbol, data)
        self.window = window
        self.num_std_dev = num_std_dev

    def generate_signals(self):
        self.signals['SMA'] = self.data['close'].rolling(window=self.window).mean()
        self.signals['Upper Band'] = self.signals['SMA'] + (self.data['close'].rolling(window=self.window).std() * self.num_std_dev)
        self.signals['Lower Band'] = self.signals['SMA'] - (self.data['close'].rolling(window=self.window).std() * self.num_std_dev)
        self.signals['price'] = self.data['close']
        self.signals['signal'] = 0.0
        self.signals.loc[self.data['close'] < self.signals['Lower Band'], ['signal']] = 1.0
        self.signals.loc[self.data['close'] > self.signals['Upper Band'], ['signal']] = -1.0

    def plot_signals(self, n_intervals=100):
        plt.figure(figsize=(14, 7))
        plt.plot(self.data['close'][-n_intervals:], label='Close Price')
        signals = self.signals[-n_intervals:]
        plt.plot(signals[signals['signal'] == 1.0].index,
                 signals['price'][signals['signal'] == 1.0],
                 '^', markersize=10, color='m', label='Buy Signal')
        plt.plot(signals[signals['signal'] == -1.0].index,
                 signals['price'][signals['signal'] == -1.0],
                 'v', markersize=10, color='k', label='Sell Signal')
        plt.title(f'{self.symbol} - Bollinger Bands Strategy')
        plt.legend()
        plt.show()

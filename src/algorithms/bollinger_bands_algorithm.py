import pandas as pd
import matplotlib.pyplot as plt
from .algorithm import Algorithm

class BollingerBandsAlgorithm(Algorithm):
    def __init__(self, symbol: str, data: pd.DataFrame, window: int, num_std_dev: int):
        super().__init__(symbol, data)
        self.window = window
        self.num_std_dev = num_std_dev

    def generate_signals(self):
        self.signals['SMA'] = self.data['Close'].rolling(window=self.window).mean()
        self.signals['Upper Band'] = self.signals['SMA'] + (self.data['Close'].rolling(window=self.window).std() * self.num_std_dev)
        self.signals['Lower Band'] = self.signals['SMA'] - (self.data['Close'].rolling(window=self.window).std() * self.num_std_dev)
        self.signals['signal'] = 0.0
        self.signals['signal'][self.data['Close'] < self.signals['Lower Band']] = 1.0
        self.signals['signal'][self.data['Close'] > self.signals['Upper Band']] = -1.0

    def plot_signals(self):
        plt.figure(figsize=(14, 7))
        plt.plot(self.data['Close'], label='Close Price')
        plt.plot(self.signals['SMA'], label='SMA')
        plt.plot(self.signals['Upper Band'], label='Upper Band')
        plt.plot(self.signals['Lower Band'], label='Lower Band')
        plt.fill_between(self.data.index, self.signals['Upper Band'], self.signals['Lower Band'], color='gray', alpha=0.3)
        plt.title(f'{self.symbol} - Bollinger Bands Strategy')
        plt.legend()
        plt.show()

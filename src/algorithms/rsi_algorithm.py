import pandas as pd
import matplotlib.pyplot as plt
from .algorithm import Algorithm

class RSIAlgorithm(Algorithm):
    def __init__(self, symbol: str, data: pd.DataFrame, period: int):
        super().__init__(symbol, data)
        self.period = period

    def generate_signals(self):
        delta = self.data['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=self.period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=self.period).mean()
        rs = gain / loss
        self.signals['RSI'] = 100 - (100 / (1 + rs))
        self.signals['price'] = self.data['close']
        self.signals['signal'] = 0.0
        self.signals.loc[self.signals['RSI'] > 70, 'signal'] = -1.0
        self.signals.loc[self.signals['RSI'] < 30, 'signal'] = 1.0

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
        plt.title(f'{self.symbol} - RSI Strategy')
        plt.legend()
        plt.show()

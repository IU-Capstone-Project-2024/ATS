import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from .algorithm import Algorithm

class MomentumStrategyAlgorithm(Algorithm):
    def __init__(self, symbol: str, data: pd.DataFrame, window: int):
        super().__init__(symbol, data)
        self.window = window

    def generate_signals(self):
        self.signals['ROC'] = self.data['close'].pct_change(periods=self.window) * 100
        self.signals['signal'] = 0.0
        self.signals['price'] = self.data['close']
        self.signals.loc[self.signals.index[self.window:], ['signal']] = np.where(self.signals['ROC'][self.window:] > 0, 1.0, 0.0)
        self.signals['positions'] = self.signals['signal'].diff()

    def plot_signals(self, n_intervals=100):
        plt.figure(figsize=(14, 7))
        plt.plot(self.data['close'][-n_intervals:], label='Close Price')
        signals = self.signals[-n_intervals:]
        plt.plot(signals[signals['positions'] == 1.0].index,
                 signals['price'][signals['positions'] == 1.0],
                 '^', markersize=10, color='m', label='Buy Signal')
        plt.plot(signals[signals['positions'] == -1.0].index,
                 signals['price'][signals['positions'] == -1.0],
                 'v', markersize=10, color='k', label='Sell Signal')
        plt.title(f'{self.symbol} - Momentum Strategy')
        plt.legend()
        plt.show()

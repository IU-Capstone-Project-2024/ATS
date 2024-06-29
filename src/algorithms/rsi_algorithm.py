import pandas as pd
import matplotlib.pyplot as plt
from .algorithm import Algorithm

class RSIAlgorithm(Algorithm):
    def __init__(self, symbol: str, data: pd.DataFrame, period: int):
        super().__init__(symbol, data)
        self.period = period

    def generate_signals(self):
        delta = self.data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=self.period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=self.period).mean()
        rs = gain / loss
        self.signals['RSI'] = 100 - (100 / (1 + rs))
        self.signals['signal'] = 0.0
        self.signals['signal'][self.signals['RSI'] > 70] = -1.0
        self.signals['signal'][self.signals['RSI'] < 30] = 1.0

    def plot_signals(self):
        plt.figure(figsize=(14, 7))
        plt.plot(self.data['Close'], label='Close Price')
        plt.plot(self.signals['RSI'], label='RSI')
        plt.axhline(y=70, color='r', linestyle='-')
        plt.axhline(y=30, color='g', linestyle='-')
        plt.title(f'{self.symbol} - RSI Strategy')
        plt.legend()
        plt.show()

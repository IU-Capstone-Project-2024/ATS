import pandas as pd

class Algorithm:
    def __init__(self, symbol: str, data: pd.DataFrame):
        self.symbol = symbol
        self.data = data
        self.signals = pd.DataFrame(index=data.index)

    def generate_signals(self):
        raise NotImplementedError("Should implement generate_signals() method")

    def backtest(self):
        raise NotImplementedError("Should implement backtest() method")

    def plot_signals(self):
        raise NotImplementedError("Should implement plot_signals() method")

    def get_signals(self):
        return self.signals

# Automatic Trade System (ATS) - Bot

Welcome to the Automatic Trade System (ATS) project! This repository is dedicated to developing a bot component of an automated trading system.

## Table of Contents

1. [Overview](#overview)
2. [Stack](#stack)
3. [Usage](#usage)
   - [Installation](#installation)
   - [Running](#running)
4. [Progress Report](#progress-report)
5. [Issues and Support](#issues-and-support)
6. [License](#license)
7. [Authors](#authors)

## Overview

The ATS project aims to develop an automated trading system that leverages machine learning algorithms to predict market trends and make informed trading decisions. The project consists of a frontend web interface and a backend machine learning component.

The bot component is a multifunctional system that performs various trading operations (buying, selling, setting orders, etc.) on the registered business account via the API, as well as monitors dynamically changing data of the cryptocurrency exchange and implements several trading strategies that are set through classical trading algorithms methodology.

## Stack
![Python](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)
![SQLite](https://img.shields.io/badge/Sqlite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)

- **Python** libraries:
 * **Quantconnect, TA-Lib, Zipline, Backtrader, PyAlgoTrade**: These libraries and frameworks are specialized for financial and trading analytics.
   * **Quantconnect** offers a cloud-based algorithmic trading platform.
   * **TA-Lib** provides technical analysis of financial market data.
   * **Zipline**, **Backtrader**, and **PyAlgoTrade** support backtesting trading algorithms.
 * **sqlite3** - This library provides tools for working with SQLite, enabling efficient storage and retrieval of our application's data.


* **Fast API, ByBit API**: FastAPI is used for creating high-performance APIs, essential for our backend. **ByBit API** allows us to interact with the binance cryptocurrency exchange for real-time trading operations.


- **SQLite** database:
 * High Write Throughput making it suitable for logging real-time trading activities.
 * high scalability and can distribute data across multiple servers, ensuring quick access and storage even under heavy loads.
 * powerful indexing and aggregation capabilities, enabling efficient querying and real-time data analysis.




## Usage

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/IU-Capstone-Project-2024/ATS_bot/
   cd ATS_bot
   ```

2. Activate virtual environment

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

### Running

To run the bot, execute the following command:

```bash
python src/bot.py
```

## Progress Report

### Done:

- Defined the techical structure of the project (creation of interfaces and basic modules): maintainable, easily addable and productive system
- Implemented algorithms:
    * SMA (Simple Moving Average) and EMA (Exponential Moving Average) - look at the moving average of buy/sell picks. They are essential tools for analyzing price trends, serving as the baseline for our decision-making process.
    * RSI (Relative Strength Index) algorithm assesses whether a coin is oversold or overbought, using a scale from 0 to 100 to inform trading actions.
    * The MACD (Moving Average Convergence Divergence) evaluates the interaction between two moving averages and signals actions when they cross.
    * Bollinger Bands analyze price volatility by considering moving averages and standard deviations, guiding our trading decisions based on price deviations from these bands.
- Connected and tested exchange API
- Added DB and transactions logging
- Created CLI for management

### To-Do:
- Merge the branches & resolve conflicts
- Add class methods to decompose the system into maintanable & atomic parts
- Up the SQLlite Database & save logs to it
- Connect trade algorithms with API interface


## Issues and Support

If you encounter any issues or need support, please open an issue in the GitHub repository.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Authors

- [Ivan Golov](https://github.com/IVproger): Team Lead
- [Andrey Pavlov](an.pavlov@innopolis.university): Algorithms Engineer
- [Shamil Kashapov](https://github.com/favelanky): Full-stack Developer
- [Bulat Latypov](https://github.com/Bulatypov): Backend Developer

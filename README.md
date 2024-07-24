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

The ATS project aims to develop an automated trading system that leverages machine learning and trading algorithms to predict market trends and make informed trading decisions. The project consists of a frontend web interface, backend machine learning and algorithmic trading component.

The bot component is a multifunctional system that performs various trading operations (buying, selling, setting orders, etc.) on the registered business account via the API, as well as monitors dynamically changing data of the cryptocurrency exchange and implements several trading strategies that are set through classical trading algorithms methodology.

Algorithmic section contains of 6 functions:
1. [SMA](https://github.com/IU-Capstone-Project-2024/ATS_bot/blob/main/src/algorithms/sma_algorithm.py)
2. [EMA](https://github.com/IU-Capstone-Project-2024/ATS_bot/blob/main/src/algorithms/ema_algorithm.py)
3. [MACD](https://github.com/IU-Capstone-Project-2024/ATS_bot/blob/main/src/algorithms/macd_algorithm.py)
4. [RSI](https://github.com/IU-Capstone-Project-2024/ATS_bot/blob/main/src/algorithms/rsi_algorithm.py)
5. [Bollinger bands](https://github.com/IU-Capstone-Project-2024/ATS_bot/blob/main/src/algorithms/bollinger_bands_algorithm.py)
6. [Momentum strategy](https://github.com/IU-Capstone-Project-2024/ATS_bot/blob/main/src/algorithms/momentum_strategy.py)


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

## Project website and progress reports:

[Innopolis University Summer course 2024 ATS capstone project](https://capstone.innopolis.university/docs/2024/ats/week1)

## Issues and Support

If you encounter any issues or need support, please open an issue in the GitHub repository.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Authors

- [Ivan Golov](https://github.com/IVproger): Team Lead
- [Andrey Pavlov](https://github.com/IAndermanI): Algorithms Engineer
- [Shamil Kashapov](https://github.com/favelanky): Full-stack Developer
- [Bulat Latypov](https://github.com/Bulatypov): Backend Developer

# metatrader5rocket
Metatrader 5 Libraries Python

## Introduction

metatrader5rocket is a python package that provides interfaces to metatrader5(mt5).

currently works with Python >= 3.6

## Feature

At the momment, metatrader5rocket supports:
- Tickers
- Orders
- Close Position
- Simple Bot

## Installation

```python
$ git clone https://github.com/sluvie/metatrader5rocket.git
$ cd metatrader5rocket
$ pip install -r requirements.txt
```
## Usage

Tickers:
```python
import metatrader.mt5 as mt5
import os

# start the engine
if __name__ == '__main__':
    # clear screen
    os.system('cls||clear')

    symbol = "XAUUSD"
    interval = "m5"
    days = 7

    engine = mt5.MT5()
    engine.start()

    # get information account
    account_info = engine.account_info()
    print("Name     : {}".format(account_info.name))
    print("Server   : {}".format(account_info.server))
    print("Company  : {}".format(account_info.company))
    print("Balances : {:.2f}".format(account_info.balance))
    print("")

    # get tickers
    ohlc = engine.tickers(symbol, interval, days)
    print(ohlc)
    print("")

    # shutdown
    engine.shutdown()
```


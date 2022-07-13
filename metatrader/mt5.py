"""
@author: sluvie
"""
import re
import MetaTrader5 as mt5
import pandas as pd
import config as conf

BUY = mt5.ORDER_TYPE_BUY
SELL = mt5.ORDER_TYPE_SELL
DEVIATION = 0

class MT5(object):

    def __init__(self):
        pass

    def run(self):
        pass

    def start(self):
        username, password, server = conf.USERNAME, conf.PASSWORD, conf.SERVER

        # display data on the MetaTrader 5 package
        print("MetaTrader5 package author: ",mt5.__author__)
        print("MetaTrader5 package version: ",mt5.__version__)
        if not mt5.initialize():
            print("initialize() failed, error code =",mt5.last_error())
            quit()

        # display data on MetaTrader 5 version
        print(mt5.version())
        print("")

        authorized = mt5.login(login=username, password=password, server=server)
        if not authorized:
            print("failed to connect at account #{}, error code: {}".format(username, mt5.last_error()))


    def shutdown(self):
        mt5.shutdown()

    # get mt5 account info
    def account_info(self):
        return (mt5.account_info())


    # get ohlc
    def tickers(self, symbol, interval, days):
        rates = []

        if interval == "m1":
            rates = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M1, 0, 15 * 96 * days)
        elif interval == "m5":
            rates = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M5, 0, 3 * 96 * days)
        elif interval == "m15":
            rates = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M15, 0, 96 * days)
        elif interval == "m30":
            rates = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M30, 0, 48 * days)
        elif interval == "h1":
            rates = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_H1, 0, 24 * days)
        elif interval == "h4":
            rates = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_H4, 0, 6 * days)
        elif interval == "d1":
            rates = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_D1, 0, 1 * days)

        # data
        data = []
        for raw in rates:
            data.append([raw['time'], raw['open'], raw['high'], raw['low'], raw['close']])

        # ohlc
        ohlc = pd.DataFrame(data)
        ohlc.columns = ['time', 'open', 'high', 'low', 'close']
        ohlc['time'] = pd.to_datetime(ohlc['time'], unit='s')
        ohlc = ohlc.set_index('time')
        ohlc.dropna()
        ohlc["Open"] = pd.to_numeric(ohlc["open"])
        ohlc["High"] = pd.to_numeric(ohlc["high"])
        ohlc["Low"] = pd.to_numeric(ohlc["low"])
        ohlc["Close"] = pd.to_numeric(ohlc["close"])
        ohlc['numeric_col'] = range(len(ohlc))

        # remove unused column
        ohlc.drop(columns=['open', 'high', 'low', 'close'], inplace=True, axis=1)

        return (ohlc)


    # get positions
    def positions(self, symbol):
        positions = mt5.positions_get(symbol=symbol)
        if len(positions) == 0:
            print("No open positions")
        return (positions)


    # orders
    def orders(self, symbol, trend, lot, price=0):

        if trend == BUY:
            # check using real price or by order
            price = mt5.symbol_info_tick(symbol).ask if price == 0 else price
            request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": symbol,
                "volume": lot,
                "type": mt5.ORDER_TYPE_BUY,
                "price": price,
                "deviation": 0,
                "magic": 0,
                "comment": "script buy",
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_IOC,
            }
            result = mt5.order_send(request)
            print(result)

        if trend == SELL:
            # check using real price or by order
            price = mt5.symbol_info_tick(symbol).bid if price == 0 else price
            request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": symbol,
                "volume": lot,
                "type": mt5.ORDER_TYPE_SELL,
                "price": price,
                "deviation": 0,
                "magic": 0,
                "comment": "script sell",
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_IOC,
            }
            result = mt5.order_send(request)
            print(result)

        print("")


    # close position
    def close_position(self, symbol, ticket, trend, lot):
        if trend == BUY:
            request= {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": symbol,
                "volume": lot,
                "type": mt5.ORDER_TYPE_SELL,
                "position": ticket,
                "price": mt5.symbol_info_tick(symbol).bid,
                "deviation": DEVIATION,
                "magic": 0,
                "comment": "close buy",
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_IOC,
            }
            result = mt5.order_send(request)
            print(result)
            print("")

        if trend == SELL:
            request= {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": symbol,
                "volume": lot,
                "type": mt5.ORDER_TYPE_BUY,
                "position": ticket,
                "price": mt5.symbol_info_tick(symbol).ask,
                "deviation": DEVIATION,
                "magic": 0,
                "comment": "close sell",
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_IOC,
            }
            result = mt5.order_send(request)
            print(result)
            print("")
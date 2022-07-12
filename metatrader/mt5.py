"""
@author: sluvie
"""
import MetaTrader5 as mt5
import pandas as pd
import config as conf

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
    def get_data(self, symbol, interval, days):
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
import metatrader.mt5 as mt5
import metatrader.indicator as ind
import os
import time
import numpy as np
import config as conf


def do_calculate(data):
    # get the EMA (9, 21, 55)
    ema_1 = ind.iMA(data, 9, 0, 'EMA')
    ema_2 = ind.iMA(data, 21, 0, 'EMA')
    ema_3 = ind.iMA(data, 55, 0, 'EMA')
    
    # get RSI data (14)
    rsi = ind.iRSI(data, 14)
    data['rsi'] = rsi

    # signals
    data['signals'] = np.where(
        (ema_1 > ema_2) & (ema_2 > ema_3) & (rsi > 51), "red", # histogram red (down)
        np.where(
            (ema_1 < ema_2) & (ema_2 < ema_3) & (rsi < 49), "green", # histogram green (up)
            "" # nothing
        )
    )
    data["over"] = np.where(
        (rsi < 30), "oversold",
        np.where(
            (rsi > 70), "overbought", ""
        )
    )

    # prediction to buy based on signals (green) and over () and over[-1] (oversold)
    data["prediction"] = np.where(
        (data.shift(1)['signals'] == "green") & (data['over'] == "") & (data.shift(1)['over'] == "oversold"), "buy", 
        np.where(
            (data.shift(1)['signals'] == "red") & (data['over'] == "") & (data.shift(1)['over'] == "overbought"), "sell", ""
        )
    )

    # calculate the average of price, max and min
    counter = len(data)
    average_low = (data['Low'].sum() / counter)
    average_high = (data['High'].sum() / counter)

    # result
    data_signals = data['signals'].iloc[-1]
    data_rsi = data['rsi'].iloc[-1]
    data_price = data['Close'].iloc[-1]
    data_prediction = data['prediction'].iloc[-1]

    # trend
    trend = mt5.BUY if (data_price <= average_low) and (data_prediction == "buy") else mt5.SELL if (data_price >= average_high) and (data_prediction == "sell") else -1
    
    return (data_price, average_low, average_high, data_rsi, trend, data_signals)


# start the engine
if __name__ == '__main__':
    # clear screen
    os.system('cls||clear')

    symbol = conf.SYMBOL
    interval = conf.INTERVAL
    days = conf.DAYS
    lot = conf.LOT

    engine = mt5.MT5()

    while True:
        engine.start()

        # get information account
        account_info = engine.account_info()
        print("Name     : {}".format(account_info.name))
        print("Server   : {}".format(account_info.server))
        print("Company  : {}".format(account_info.company))
        print("Balances : {:.5f}".format(account_info.balance))
        print("")

        # get tickers
        ohlc = engine.tickers(symbol, interval, days)
        
        # analysis for next order
        price, avg_low, avg_high, rsi, trend, signals = do_calculate(ohlc)
        print("RSI      : {:.5f}".format(rsi))
        print("Price    : {:.5f}".format(price))
        print("Avg.Low  : {:.5f}".format(avg_low))
        print("Avg.High : {:.5f}".format(avg_high))
        print("Signals  : {}".format(signals))
        print("Trend    : {}".format("buy" if trend == mt5.BUY else "sell" if trend == mt5.SELL else ""))
        print("")

        # try do order
        # ?: example for order
        # ?: validation, only one transaction
        positions = engine.positions(symbol)
        if len(positions) == 0:
            # can order
            if trend == -1:
                pass
            else:
                engine.orders(symbol, trend, lot)
        else:
            print("can't order, only one transaction allowed")
            print("")

        # try to close, if profit
        for position in positions:
            print("Ticket           : {}".format(position.ticket))
            print("Price (Open)     : {:.5f}".format(position.price_open))
            print("Volume           : {:.5f}".format(position.volume))
            print("Profit           : {:.5f}".format(position.profit))
            print("")

            # take profit
            if position.profit > conf.TP and trend == -1 and signals == "":
                engine.close_position(symbol, position.ticket, position.type, lot)
            # cut loss
            if position.profit < conf.SL and trend == -1 and signals == "":
                engine.close_position(symbol, position.ticket, position.type, lot)

        # shutdown
        engine.shutdown()

        print("")
        print("wait for 10 seconds")
        print("")
        time.sleep(10)
import metatrader.mt5 as mt5
import os

# start the engine
if __name__ == '__main__':
    # clear screen
    os.system('cls||clear')

    symbol = "XAUUSD"
    interval = "m5"
    days = 7
    lot = 0.01
    profit = 0.2

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

    # try do order
    # ?: example for order
    # engine.orders(symbol, mt5.BUY, lot)
    # engine.orders(symbol, mt5.SELL, lot)

    # get positions
    positions = engine.positions(symbol)
    print("")

    # try to close, if profit
    for position in positions:
        print("Ticket           : {}".format(position.ticket))
        print("Price (Open)     : {:.2f}".format(position.price_open))
        print("Price (Current)  : {:.2f}".format(position.price_current))
        print("Volume           : {:.2f}".format(position.volume))
        print("Profit           : {:.2f}".format(position.profit))
        print("")

        if position.profit > profit:
            engine.close_position(symbol, position.ticket, position.type, lot)

    # shutdown
    engine.shutdown()
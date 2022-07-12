import metatrader.mt5 as mt5
import os

# start the engine
if __name__ == '__main__':
    # clear screen
    os.system('cls||clear')

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
    ohlc = engine.get_data("XAUUSD", "m5", 7)
    print(ohlc)

    engine.shutdown()
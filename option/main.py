__author__ = 'sarra souissi'

from option.binomial.binomial_option import BinaryOption
from option.market_data import MarketData
from option.option import Option

if __name__ == '__main__':
    underlying_price = 31  # index level
    strike = 30  # option_valuation strike
    maturity = 0.75  # maturity date
    r = 0.05  # risk-less short rate
    volatility = 0.3  # volatility
    steps = 3 #Steps
    style = 1
    asset = 1
    option_type = 2
    str_strike = input("Strike K (default Value " + str(strike) + "): ")
    if (str_strike != "") :
        strike = float(str_strike)

    str_underlying_price = input("Price S0 (default Value " + str(underlying_price) + "): ")
    if (str_underlying_price != "") :
        underlying_price = float(str_underlying_price)

    str_maturity = input("Maturity (in Years) (default Value " + str(maturity) + "): ")
    if (str_maturity != "") :
        maturity = float(str_maturity)


    str_r = input("Risk-less short rate r (default Value "+str(r)+"): ")
    if (str_r != "") :
        r = float(str_r)

    str_volatility = input("Volatility (default Value " + str(volatility) + "): ")
    if (str_volatility != "") :
        volatility = float(str_volatility)

    str_n = input("Steps (Default Value " + str(steps) + "): ")
    if (str_n != "") :
        steps = int(str_n)

    str_style = input("style (Default Value "+str(style)+"): [1: Europeen, 2: American] ")
    if (str_style != "") :
        style = int(str_style)

    str_type = input("Type (Default Value " + str(option_type) + "):   [1: Call, 2: Put]")
    if (str_type != "") :
        option_type = int(str_type)

    str_asset = input("Asset [0: Equity , 1: Bond , 2 :Equity  paying dividends ,"
                      "3: Index ,  4: Future  ,5: Commodity , "
                     "6: Currency]  (Default Value"+ str(asset)+"): ")

    if str_asset != "":
        asset = int(str_asset)

        str_q = ""
        if (asset == 2 or asset == 3) :
            while str_q == "":
                str_q = input("Average dividend yield over the option life:")
            q = float(str_q)

        if asset == 6 :
            str_rf = input("[Currency option] Foreign interest rate:")
            rf = float(str_rf)

    marketData = MarketData(r, volatility)
    option = Option(option_type, style, underlying_price, strike, maturity, volatility)

    str_valuation_method = input("Valuation method [1:Binomial , 2: , 3: , 4: ]"
                                 " (Default Value"+ str(asset)+"): ")
    if str_valuation_method == "1":
        str_steps = input("Steps (Default Value " + str(steps) + "): ")
        if (str_steps != "") :
            steps = int(str_steps)

        binomial_stock_option = BinaryOption(option_type, style, underlying_price, strike, maturity, volatility, asset,marketData, steps)





__author__ = 'Olivier Lefebvre, Sarra Souissi'


class Option:
    """
    Class that stores option-related data
    """

    def __init__(self, option_type=1, style=1, underlying_price=100.0, strike=100.0, maturity=2.0,
                 implied_volatility=0.2, asset=1):
        """
        Default option constructor
        :param option_type: int
        type of the option, 1: Call, 2: Put
        :param style: int
        style of the option, 1: Europeen 2: American
        :param underlying_price: float
        price of the underlying at time 0
        :param strike: float
        strike price (exercise price)
        :param maturity: float
        time to maturity  (in years)
        :param implied_volatility: float
        implied volatility
        :param asset :int
        0: Equity , 1: Bond , 2 :Equity  paying dividends , 3: Index ,  4: Future  ,5: Commodity , 6: Currency
        :return: a new instance of the option class with the specified parameters
        """
        self.option_type = option_type
        self.style = style
        self.underlying_price = underlying_price
        self.strike = strike
        self.maturity = maturity
        self.implied_volatility = implied_volatility
        self.asset = asset
        self.C0 = None

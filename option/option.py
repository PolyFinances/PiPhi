__author__ = 'Olivier Lefebvre'

import matplotlib.pyplot as plt


class Option:
    """
    Class that stores option-related data
    """

    def __init__(self, option_type='call', style='european', underlying_price=100.0, strike=100.0, maturity=2.0,
                 implied_volatility=0.2):
        """
        Default option constructor
        :param option_type: string
        type of the option, either 'call' or 'put'
        :param style: string
        style of the option, either 'european' or 'american'
        :param underlying_price: float
        price of the underlying
        :param strike: float
        strike price
        :param maturity: float
        maturity (in years)
        :param implied_volatility: float
        implied volatility
        :return: a new instance of the option class with the specified parameters
        """
        self.option_type = option_type
        self.style = style
        self.underlying_price = underlying_price
        self.strike = strike
        self.maturity = maturity
        self.implied_volatility = implied_volatility
        self.C0 = None

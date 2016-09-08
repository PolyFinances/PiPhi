#
# Black-Scholes-Merton (1973) European Call & Put Valuation
# 05_com/BSM_option_valuation.py
#
# (c) Dr. Yves J. Hilpisch
# Derivatives Analytics with Python
#

import math
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
mpl.rcParams['font.family'] = 'serif'
from scipy.integrate import quad
from valuation.market_data import MarketData
from valuation.option import Option

__author__ = "Alexis Paquette"


# Helper Functions
def dN(x):
    """ Probability density function of standard normal random variable x."""
    return math.exp(-0.5 * x ** 2) / math.sqrt(2 * math.pi)


def N(d):
    """ Cumulative density function of standard normal random variable x."""
    return quad(lambda x: dN(x), -20, d, limit=50)[0]


# Valuation Functions
def BSM_value(Option, MarketData):
    """ Calculates Black-Scholes-Merton European call or put option value.
    Parameters
    ==========
    Option: Class Option
    MarketData:  Class MarketData

    Returns
    =======
    call_value:  float
    put_value:   float
    """
    St = Option.underlying_price
    K = Option.strike
    t = 0
    T = Option.maturity
    r = MarketData.r
    sigma = MarketData.volatility

    d1 = (math.log(St / K) + (r + 0.5 * sigma ** 2) * (T - t)) / (sigma * math.sqrt(T - t))
    d2 = d1 - sigma * math.sqrt(T - t)
    call_value = St * N(d1) - math.exp(-r * (T - t)) * K * N(d2)
    if Option.option_type == 1:
        return call_value

    elif Option.option_type == 2:
        put_value = call_value - St + math.exp(-r * (T - t)) * K
        return put_value


# Plotting European Option Values
def plot_values(Option, MarketData):
    """ Plots European option values for different parameters"""
    plt.figure(figsize=(10, 8.3))
    points = 100
    #
    # Model Parameters
    # C(K) plot
    plt.subplot(221)
    klist = np.linspace(Option.strike - 20, Option.strike + 20, points)
    vlist = []
    for K in klist:
        Option.strike = K
        vlist.append(BSM_value(Option, MarketData))
    Option.strike -= 20
    plt.plot(klist, vlist)
    plt.grid()
    plt.xlabel('strike $K$')
    plt.ylabel('present value')

    # C(T) plot
    plt.subplot(222)
    tlist = np.linspace(0.0001, Option.maturity, points)
    vlist = []
    for T in tlist:
        Option.maturity = T
        vlist.append(BSM_value(Option, MarketData))
    plt.plot(tlist, vlist)
    plt.grid(True)
    plt.xlabel('maturity $T$')
    #
    # C(r) plot
    plt.subplot(223)
    rlist = np.linspace(0, 0.1, points)
    rate = MarketData.r
    vlist = []
    for R in rlist:
        MarketData.r = R
        vlist.append(BSM_value(Option, MarketData))
    MarketData.r = rate
    plt.plot(rlist, vlist)
    plt.grid(True)
    plt.xlabel('short rate $r$')
    plt.ylabel('present value')
    plt.axis('tight')
    #
    # C(sigma) plot
    plt.subplot(224)
    sigmalist = np.linspace(0.001, 0.5, points)
    sig = MarketData.volatility
    vlist = []
    for sigma in sigmalist:
        MarketData.volatility = sigma
        vlist.append(BSM_value(Option, MarketData))
    MarketData.volatility = sig
    plt.plot(sigmalist, vlist)
    plt.grid(True)
    plt.xlabel('volatility $\sigma$')
    plt.show()


# Implied volatility
def implied_volatility(Option, MarketData, value):
    """ Calculates the implied volatility by reversing Black-Scholes-Merton model.

    Parameters
    ==========
    Option: Class Option
    MarketData:  Class MarketData
    value: option value

    Returns
    =======
    MarketData.volatility:  float
    error:   float
    """
    error = 100
    precision = 0.001
    sigmaL = min(0.001, precision)
    sigmaH = 5
    n = 0
    while abs(error) >= precision and n < 10000:
        MarketData.volatility = (sigmaL+sigmaH)/2
        approxM = BSM_value(Option, MarketData)
        if approxM > value:
            sigmaH = MarketData.volatility

        elif approxM < value:
            sigmaL = MarketData.volatility

        error = abs(approxM - value)
        n += 1
    return MarketData.volatility, error


def dividend_actualisation(div, t, r=0.05):
    """Give the actualized value of a dividend.

    Parameters
    ======================
    div: float
    t: float
    r: float

    Returns
    ======================
    div_actualized: float
    """
    div_actualised = div * math.exp(-t * r)
    return div_actualised


if __name__ == "__main__":
    option_1 = Option()
    option_1.maturity = 1
    option_1.strike = 100
    option_1.underlying_price = 100
    option_1.option_type = 1
    market_1 = MarketData()
    market_1.volatility = 0.2
    market_1.r = 0.05
    print(BSM_value(option_1, market_1))
    plot_values(option_1, market_1)


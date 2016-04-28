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


# Helper Functions
def dN(x):
    """ Probability density function of standard normal random variable x."""
    return math.exp(-0.5 * x ** 2) / math.sqrt(2 * math.pi)


def N(d):
    """ Cumulative density function of standard normal random variable x."""
    return quad(lambda x: dN(x), -20, d, limit=50)[0]


# Valuation Functions
def BSM_call_value(St, K, t, T, r, sigma):
    """ Calculates Black-Scholes-Merton European call option value.
    Parameters
    ==========
    St: float
        stock/index level at time t
    K:  float
        strike price
    t:  float
        valuation date
    T:  float
        date of maturity/time-to-maturity if t = 0; T > t
    r:  float
        constant, risk-less short rate
    sigma:  float
        volatility

    Returns
    =======
    call_value:  float
        European call present value at t
    """
    d1 = (math.log(St / K) + (r + 0.5 * sigma ** 2) * (T - t)) / (sigma * math.sqrt(T - t))
    d2 = d1 - sigma * math.sqrt(T - t)
    call_value = St * N(d1) - math.exp(-r * (T - t)) * K * N(d2)
    return call_value


def BSM_put_value(St, K, t, T, r, sigma):
    """Calculates Black-Scholes-Merton European put option value.
    Parameters
    ==========
    St: float
        stock/index level at time t
    K:  float
        strike price
    t:  float
        valuation date
    T:  float
        date of maturity/time-to-maturity if t = 0; T > t
    r:  float
        constant, risk-less short rate
    sigma: float
        volatility

    Returns
    =======
    put_value: float
    European put present value at t
    """
    put_value = BSM_call_value(St, K, t, T, r, sigma) - St + math.exp(-r * (T - t)) * K
    return put_value


# Plotting European Option Values
def plot_values(function):
    """ Plots European option values for different parameters"""
    plt.figure(figsize=(10, 8.3))
    points = 100
    #
    # Model Parameters
    #
    St = 100.0  # index level
    K = 100.0  # option strike
    t = 0.0  # valuation date
    T = 1.0  # maturity date
    r = 0.05  # risk-less short rate
    sigma = 0.2  # volatility

    # C(K) plot
    plt.subplot(221)
    klist = np.linspace(80, 120, points)
    vlist = [function(St, K, t, T, r, sigma) for K in klist]
    plt.plot(klist, vlist)
    plt.grid()
    plt.xlabel('strike $K$')
    plt.ylabel('present value')
    # C(T) plot
    plt.subplot(222)
    tlist = np.linspace(0.0001, 1, points)
    vlist = [function(St, K, t, T, r, sigma) for T in tlist]
    plt.plot(tlist, vlist)
    plt.grid(True)
    plt.xlabel('maturity $T$')

    # C(r) plot
    plt.subplot(223)
    rlist = np.linspace(0, 0.1, points)
    vlist = [function(St, K, t, T, r, sigma) for r in rlist]
    plt.plot(tlist, vlist)
    plt.grid(True)
    plt.xlabel('short rate $r$')
    plt.ylabel('present value')
    plt.axis('tight')

    # C(sigma) plot
    plt.subplot(224)
    slist = np.linspace(0.01, 0.5, points)
    vlist = [function(St, K, t, T, r, sigma) for sigma in slist]
    plt.plot(slist, vlist)
    plt.grid(True)
    plt.xlabel('volatility $\sigma$')
    plt.show()


# Implied volatility
def implied_volatility_call(St, K, t, T, r, call_value, precision=0.001):
    error = 100
    sigmaL = min(0.001, precision)
    sigmaH = 1
    while abs(error) >= precision:
        sigmaM = (sigmaL+sigmaH)/2
        approxM = BSM_call_value(St, K, t, T, r, sigmaM)
        if approxM > call_value:
            sigmaH = sigmaM

        elif approxM < call_value:
            sigmaL = sigmaM

        error = abs(approxM-call_value)

    return sigmaM, error


def implied_volatility_put(St, K, t, T, r, put_value, precision=0.001):
    error = 100
    sigmaL = min(0.001, precision)
    sigmaH = 1
    while abs(error) >= precision:
        sigmaM = (sigmaL+sigmaH)/2
        approxM = BSM_put_value(St, K, t, T, r, sigmaM)
        if approxM > put_value:
            sigmaH = sigmaM

        elif approxM < put_value:
            sigmaL = sigmaM

        error = abs(approxM-put_value)

    return sigmaM, error


# r is usually around 0.5%
def dividend_actualisation(div, t, r):
    div_actualised = div * math.exp(-t * r)
    return div_actualised



# plot_values(BSM_put_value)
# a, b = implied_volatility_put(762.16, 745, 0, 3.25/52, 0.0047, 34)
# print(a, b)
# c = BSM_put_value(762.16, 745, 0, 3.25/52, 0.005, a)
# print(c)

# print(implied_volatility_call(735.3, 740, 0, 122/254, 0.0047, 50))

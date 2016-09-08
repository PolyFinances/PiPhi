__author__ = "Olivier Lefebvre"
from math import exp, sqrt


class BinomialValuation:

    @staticmethod
    def get_binomial_parameters(option, M, market_data):
        # Time Parameters
        dt = option.T / M  # length of time interval
        df = exp(-market_data.r * dt)  # discount per interval
        # Binomial Parameters
        u = exp(market_data.sigma * sqrt(dt))  # up movement
        d = 1 / u  # down movement
        q = (exp(market_data.r * dt) - d) / (u - d)  # martingale branch probability
        return dt, df, u, d, q

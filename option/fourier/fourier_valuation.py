__author__ = "Olivier Lefebvre"

import math
import numpy as np
from numpy.fft import fft, ifft
from option.binomial.binomial_valuation import BinomialValuation as bn

class Fourier:

    @staticmethod
    def valuate_option(option, M, market_data):
        """

        :param M:
        :return:
        """

        dt, df, u, d, q = bn.get_binomial_parameters(option, M, market_data)

        # Array Generation for Stock Prices
        mu = np.arange(M + 1)
        mu = np.resize(mu, (M + 1, M + 1))
        md = np.transpose(mu)
        #Fourier- Based Option Pricing 125
        mu = u ** (mu - md)
        md = d ** md
        S = option.S0 * mu * md
        # Valuation by fft
        CT = np.maximum(S[:, -1] - option.K, 0)
        qv = np.zeros(M + 1, dtype= np.float)
        qv[0] = q
        qv[1] = 1 - q

        C0 = fft(math.exp(-market_data.r * option.T) * ifft(CT) * fft(qv) ** M)
        # Results Output
        print("Value of European option is %8.3f" % np.real(C0[0]))
        option.C0 = C0[0]
        return C0[0]
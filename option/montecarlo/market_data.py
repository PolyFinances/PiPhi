__author__ = "Olivier Lefebvre"
import numpy as np


class MarketData:
    """
    Class to hold market-related data
    """

    def __init__(self, r=0.05, volatility=0.2, rho=None, theta=None, kappa=None, std_volatility=None):
        """
        Default constructor
        :param r: float
        free-risk short rate (0.05 for example)
        :param volatility: float
        :param rho: float
        :param theta: float
        :param kappa: float
        :param std_volatility: float
        :return: a new instance of the market data class with specified parameters
        """
        self.r = r
        self.volatility = volatility
        self.rho = rho
        self.theta = theta
        self.kappa = kappa
        self.std_volatility = std_volatility

        #Computation of correlation if needed. The cholesky matrix allows to correlate numbers
        #with the correlation specified by rho
        if self.rho is not None:
            corr_mat = np.zeros((2, 2))
            corr_mat[0, :] = [1.0, rho]
            corr_mat[1, :] = [rho, 1.0]
            self.cholesky_matrix = np.linalg.cholesky(corr_mat)
        else:
            self.cholesky_matrix = None
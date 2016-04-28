__author__ = "Olivier Lefebvre"

import numpy as np


class RandomNumberGenerator:
    """
    Class to generate random number.
    """
    @staticmethod
    def generate_standard_normal(sets, time_intervals, number_paths, anti_paths=True, moment_matching=True):
        """ Function to generate random numbers following a standard normal distribution.
        Parameters
        ==========
        sets : int
        number of different set of random variables to be generated
        time_intervals : int
        number of time intervals for discretization
        number_paths : int
        number of paths to be simulated
        anti_paths: Boolean
        use of antithetic variates
        moment_matching : Boolean
        use of moment matching
        """
        if anti_paths is True:
            sn = np.random.standard_normal((sets, time_intervals, number_paths / 2))
            sn = np.concatenate((sn, -sn), axis=2)
        else:
            sn = np.random.standard_normal((sets, time_intervals, number_paths))
        if moment_matching is True:
            sn = sn - np.mean(sn)
            sn = sn / np.std(sn)
        if sets == 1:
            return sn[0]
        else:
            return sn

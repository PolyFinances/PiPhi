__author__ = "Olivier Lefebvre"
import matplotlib.pyplot as plt
import numpy as np

from valuation.montecarlo import random_number_generator as rng


class MonteCarloSimulation:
    """
    Class responsible for Monte Carlo simulation
    """

    def __init__(self, option, market_data, stochastic_volatility=False, time_intervals=50, paths=50000):
        """
        Class default constructor
        :param option: Option
        :param market_data: MarketData
        :param stochastic_volatility: bool
        :param time_intervals: int
        :param paths: int
        :return:
        """
        self.option = option
        self.market_data = market_data
        self.stochastic_volatility = stochastic_volatility
        self.time_intervals = time_intervals
        self.paths = paths
        self.gbm_paths = None
        self.srd_paths = None

        if stochastic_volatility:
            if market_data.rho is None or market_data.cholesky_matrix is None or market_data.theta is None \
                    or market_data.kappa is None:
                print("Error parsing market data.")
            else:
                self.random_numbers = rng.generate_standard_normal(2, self.time_intervals, self.paths)
                self.rn_set_brownian = 0
                self.rn_set_volatility = 1

    def generate_geometric_brownian_motion_paths(self):
        """
        Method to generate path following a geometric brownian motion
        to model the option's underlying's movement
        :return:
        """
        # array initialization for path simulation
        paths = np.zeros((self.time_intervals, self.paths))
        # initialize first date with initial value
        paths[0] = self.option.underlying_price
        # if the stochastic volatility is taken into consideration, generate square root diffusion paths for it and
        # select previously generated random numbers for correlation
        if self.stochastic_volatility is False:
            random_numbers = rng.generate_standard_normal(1, self.time_intervals, self.paths)
        else:
            random_numbers = self.random_numbers
            self.generate_square_root_diffusion_paths()

        dt = self.option.maturity / self.time_intervals
        for t in range(1, self.time_intervals):
            # select the right time slice from the relevant random number set and the right volatility
            if self.stochastic_volatility is False:
                ran = random_numbers[t]
                volatility = self.market_data.volatility
            else:
                ran = np.dot(self.market_data.cholesky_matrix, random_numbers[:, t, :])
                ran = ran[self.rn_set_brownian]
                volatility = self.srd_paths[t]
            # step computation
            paths[t] = paths[t - 1] * np.exp((self.market_data.r - 0.5 * volatility ** 2) * dt +
                                             volatility * np.sqrt(dt) * ran)
        self.gbm_paths = paths

    def generate_square_root_diffusion_paths(self):
        """
        Function to generate square-root diffusion paths to model the
        volatility's stochastic aspect
        :return:
        """
        # array initialization with initial value
        paths = np.zeros((self.time_intervals, self.paths))
        paths_ = np.zeros_like(paths)
        paths[0] = self.market_data.volatility
        paths_[0] = self.market_data.volatility

        if self.stochastic_volatility is False:
            random_numbers = rng.generate_standard_normal(1, self.time_intervals, self.paths)
        else:
            random_numbers = self.random_numbers

        dt = self.option.maturity / self.time_intervals
        for t in range(1, self.time_intervals):
            # select the right time slice from the relevant random number set
            if self.stochastic_volatility is False:
                ran = random_numbers[t]
            else:
                ran = np.dot(self.market_data.cholesky_matrix, random_numbers[:, t, :])
                ran = ran[self.rn_set_volatility]
            # step computation
            # full truncation Euler discretization
            paths_[t] = (paths_[t - 1] + self.market_data.kappa *
                         (self.market_data.theta - np.maximum(0, paths_[t - 1, :])) * dt +
                         np.sqrt(np.maximum(0, paths_[t - 1, :])) * self.market_data.std_volatility *
                         np.sqrt(dt) * ran)
            paths[t] = np.maximum(0, paths_[t])
        self.srd_paths = paths

    def valuate_option(self, basic_functions=5):
        """
        Function to price an option based on the Monte Carlo simulation
        :param basic_functions: int
        the number of basic functions to use with the least square optimizer
        :return:
        """
        if self.gbm_paths is None:
            self.generate_geometric_brownian_motion_paths()

        if self.option.option_type == 'call':
            h = np.maximum(self.gbm_paths - self.option.strike, 0)
        elif self.option.option_type == 'put':
            h = np.maximum(self.option.strike - self.gbm_paths, 0)
        else:
            print("Error parsing option: option_type must be either 'call' or 'put'")
            return

        if self.option.style == "european":
            # MCS estimator
            self.option.C0 = np.exp(-self.market_data.r * self.option.maturity) * np.sum(h[-1]) / self.paths
        elif self.option.style == "american":
            # LSM algorithm
            V = np.copy(h)
            dt = self.option.maturity / self.time_intervals
            df = np.exp(-self.market_data.r * dt)
            for t in range(self.time_intervals - 2, 0, - 1):
                reg = np.polyfit(self.gbm_paths[t], V[t + 1] * df, basic_functions)
                C = np.polyval(reg, self.gbm_paths[t])
                V[t] = np.where(C > h[t], V[t + 1] * df, h[t])
            # MCS estimator
            self.option.C0 = df * np.sum(V[1]) / self.paths
        else:
            print("Error parsing option: option_style must be either 'european' or 'american'")
            return

    def plot_paths_distribution(self, nb_bins=50, normed=True):
        """
        Method to show distribution of paths final values
        :return:
        """

        if normed:
            ylabel="Normalized sum"
        else:
            ylabel="Sum"

        plt.figure()
        if self.stochastic_volatility:
            plt.subplot(211)
            plt.hist(self.gbm_paths[-1], nb_bins, normed=normed, histtype='bar', rwidth=0.8)
            plt.ylabel(ylabel)
            plt.title("Final underlying value of simulated Monte Carlo paths (geometric brownian motion)")

            plt.subplot(212)
            plt.hist(self.srd_paths[-1], nb_bins, normed=normed, histtype='bar',rwidth=0.8)
            plt.ylabel(ylabel)
            plt.xlabel("Path final value")
            plt.title("Final volatility value of simulated Monte Carlo paths (square-root diffusion)")
        else:
            plt.hist(self.gbm_paths[-1], nb_bins, normed=normed, histtype='bar', rwidth=0.8)
            plt.ylabel(ylabel)
            plt.xlabel("Path final value")
            plt.title("Final underlying value of simulated Monte Carlo paths (geometric brownian motion)")
        plt.draw()

    def plot_paths_graphs(self, nb_paths=10):
        """
        Function to show path motion in graphs
        :param nb_paths: int
        number of paths to show
        :return:
        """
        plt.figure()
        if self.stochastic_volatility:
            sub1 = plt.subplot(211)
            plt.plot(np.arange(0, self.option.maturity, self.option.maturity / self.time_intervals),
                     self.gbm_paths[:, :nb_paths])
            plt.grid(True)
            plt.ylabel("Underlying price")
            plt.title("Simulated Monte Carlo paths for underlying (geometric brownian motion)")
            plt.setp(sub1.get_xticklabels(), visible=False)
            plt.subplot(212)
            plt.plot(np.arange(0, self.option.maturity, self.option.maturity / self.time_intervals),
                     self.srd_paths[:, :nb_paths])
            plt.axhline(self.market_data.theta, color='r', ls='--', lw=2.0)
            plt.grid(True)
            plt.ylabel("Volatility")
            plt.xlabel("Time (years)")
            plt.title("Simulated Monte Carlo paths for volatility (square-root diffusion)")
        else:
            plt.plot(np.arange(0, self.option.maturity, self.option.maturity / self.time_intervals),
                     self.gbm_paths[:, :nb_paths])
            plt.grid(True)
            plt.ylabel("Underlying price")
            plt.xlabel("Time (years)")
            plt.title("Simulated Monte Carlo paths for underlying (geometric brownian motion)")
        plt.draw()

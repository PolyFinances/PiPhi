__author__ = 'sarra souissi'
import math


class Option:

    def __init__(self, S0, K, T, r, sigma, steps=3, style=1, type=1, asset=0):
        """
        class attributes:
        S0: float
            stock/index level at time 0
        K:  float
            strike price (exercise price)
        T:  float
            date of maturity/time-to-maturity if t = 0; T > t
        r:  float
            constant, risk-less short rate
        q:  float
            constant, foreing risk-less short rate
        sigma: float
            volatility
        style:  1: Europeen
                2: American
        type :  1: Call
                2: Put
        asset:  0: Equity option
                1: Bond option
                2: Equity option paying dividends
                3: Stock index option
                4: Future option
                5: Commodity option
                6: Currency option

        """
        self.__S0 = S0
        self.__K = K
        self.__T = T
        self.__r = r
        self.__sigma = sigma
        self.__style = style
        self.__type = type
        self.__asset = asset
        self.__steps = steps
        str_q = ""
        if (asset == 2 or asset == 3) :
            while   str_q == "" :
                str_q = input("Average dividend yield over the option life:")
            self.__q = float(str_q)

        if asset == 6 :
            str_rf = input("[Currency option] Foreign interest rate:")
            self.__rf = float(str_rf)

    @property
    def S0(self):
        return  self.__S0

    @property
    def K(self):
        return self.__K

    @property
    def r(self):
        return self.__r
    @property
    def T(self):
        return self.__T

    @property
    def sigma(self):
        return self.__sigma

    @property
    def type(self):
        return self.__type

    def get_str_type(self):
        dic = {1: "Call", 2: "Put"}
        if self.type in dic.keys():
            return dic [self.type]

    @property
    def style(self):
        return self.__style

    @property
    def q (self):
        return self.__q

    @property
    def rf (self):
        return self.__rf

    def get_str_style(self):
        dic = {1: "Europeen", 2: "American"}
        if self.style in dic.keys():
            return dic [self.style]

    @property
    def asset(self):
        return self.__asset

    def get_str_asset(self):
        dic = {0: "Equity ",1: "Bond ", 2 :"Equity  paying dividends" ,
              3: "Index ",  4: "Future " ,5: "Commodity ", 6: "Currency " }

        if self.asset in dic.keys():
            return dic [self.asset]

    @property
    def steps(self):
        return self.__steps

    def __repr__(self):
        return str(self.S0)

    def getDown(self):

        return math.exp(-self.sigma * math.sqrt(self.T / self.steps))

    def getUp(self):
        print("getUp" + str(self.sigma) + ", " + str(self.T/self.steps))
        return math.exp(self.sigma * math.sqrt(self.T/self.steps))

    def callPayOff(self,St):
        return max(St - self.K, 0.0)

    def putPayOff(self,St):
        return max(self.K - St, 0.0)

    def payOff(self,St):
        if self.type == 1 : # Call
            return self.callPayOff(St)
        else :
            return self.putPayOff(St)

    def riskNeutralProbability(self):
        up = self.getUp()
        down = self.getDown()
        if self.asset in [0, 1]:
            return (math.exp(self.r*self.T/self.steps) - down)/(up-down)
        if self.asset in [2, 3]:
            return (math.exp((self.r-self.q)*self.T/self.steps) - down)/(up-down)
        if self.asset in [4, 5]:
            return (1 - down)/(up-down)
        if self.asset == 6:
            return (math.exp((self.r-self.rf)*self.T/self.steps) - down)/(up-down)

    def __repr__(self):
        st = "Stock price S0 :" +str(self.S0) + \
        "       Strike K :" +str(self.K)  +"\n Risk-less short rate r : " + str(self.r*100) +\
               "%\n Maturity (in Years) T :" +str(self.T)  + "        Steps n : " + str(self.steps) + \
               " \n Volatility sigma : " +str(self.sigma * 100)+ \
               "%    [ u="+ str(round(self.getUp(),2)) + \
               ",    d=" +str(round(self.getDown(),2)) +\
               ",    p=" + str(round(self.riskNeutralProbability(),2))+" ]" +\
               "\n Type : " + self.get_str_type() + \
               "         Style : " +self.get_str_style()+\
               "        Asset : " + self.get_str_asset()
        if self.asset == 6:
            st += " [rf =" + str(self.rf*100) + "%]"

        if self.asset in [2, 3]:
            st += " [q =" + str(self.q*100) + "%]"
        return st


if __name__ == '__main__':

    S0 = 100.0  # index level
    K = 100.0  # option_valuation strike
    T = 1.0  # maturity date
    r = 0.05  # risk-less short rate
    sigma = 0.2  # volatility
    n = 4 # Steps
    stock_option = Option(S0, K, T, r, sigma,n)
    print(stock_option)
    print(stock_option.getUp())
    print(stock_option.getDown())
    print(stock_option.riskNeutralProbability())

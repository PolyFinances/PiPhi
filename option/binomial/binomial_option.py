__author__ = 'Sarra Souissi'
import math
from src.option.option import Option
from src.option.montecarlo.market_data import MarketData

class BinaryOption (Option):

    def __init__(self, option_type, style, underlying_price, strike, maturity, volatility,asset, market_data, steps):
        Option.__init__(self,option_type, style, underlying_price, strike, maturity, volatility, asset)
        self.steps = steps
        self.market_data = market_data

    #@property
    #def S0(self):
    #   return  self

    #@property
    #def K(self):
    #    return self.__K

#    @property
 #   def r(self):
 #       return self.__r
  #  @property
  #  def T(self):
  #      return self.__T

   # @property
   # def sigma(self):
   #     return self.__sigma

    #@property
    #def type(self):
    #    return self.__type

    #def get_str_type(self):
    #    dic = {1: "Call", 2: "Put"}
    #    if self.type in dic.keys():
    #        return dic [self.type]

    #@property
    #def style(self):
    #    return self.__style

    #@property
    #def q (self):
    #    return self.__q

    #@property
    #def rf (self):
   #     return self.__rf

    #def get_str_style(self):
    #    dic = {1: "Europeen", 2: "American"}
    #    if self.style in dic.keys():
    #        return dic [self.style]

    #@property
    #def asset(self):
    #    return self.__asset

    #def get_str_asset(self):
    #    dic = {0: "Equity ",1: "Bond ", 2 :"Equity  paying dividends" ,
    #          3: "Index ",  4: "Future " ,5: "Commodity ", 6: "Currency " }

     #   if self.asset in dic.keys():
     #       return dic [self.asset]

    #@property
    #def steps(self):
    #    return self.__steps

    #def __repr__(self):
    #    return str(self.S0)

    def getDown(self):
        return math.exp(-self.implied_volatility * math.sqrt(self.maturity / self.steps))

    def getUp(self):
        return math.exp(self.implied_volatility * math.sqrt(self.maturity/self.steps))

    def callPayOff(self,St):
        return max(St - self.strike, 0.0)

    def putPayOff(self,St):
        return max(self.strike - St, 0.0)

    def payOff(self,St):
        if self.option_type == 1 : # Call
            return self.callPayOff(St)
        else :
            return self.putPayOff(St)

    def riskNeutralProbability(self):
        up = self.getUp()
        down = self.getDown()
        if self.asset in [0, 1]:
            return (math.exp(self.market_data.r*self.maturity/self.steps) - down)/(up-down)
        if self.asset in [2, 3]:
            return (math.exp((self.market_data.r-self.q)*self.maturity/self.steps) - down)/(up-down)
        if self.asset in [4, 5]:
            return (1 - down)/(up-down)
        if self.asset == 6:
            return (math.exp((self.market_data.r-self.rf)*self.maturity/self.steps) - down)/(up-down)

    #def __repr__(self):
        #st = "Stock price S0 :" +str(self.S0) + \
        #"       Strike K :" +str(self.K)  +"\n Risk-less short rate r : " + str(self.r*100) +\
        #       "%\n Maturity (in Years) T :" +str(self.T)  + "        Steps n : " + str(self.steps) + \
        #       " \n Volatility sigma : " +str(self.sigma * 100)+ \
        #       "%    [ u="+ str(round(self.getUp(),2)) + \
        #       ",    d=" +str(round(self.getDown(),2)) +\
        #       ",    p=" + str(round(self.riskNeutralProbability(),2))+" ]" +\
        #       "\n Type : " + self.get_str_type() + \
        #       "         Style : " +self.get_str_style()+\
        #       "        Asset : " + self.get_str_asset()
        #if self.asset == 6:
        #    st += " [rf =" + str(self.rf*100) + "%]"

        #if self.asset in [2, 3]:
        #    st += " [q =" + str(self.q*100) + "%]"
        #return st


if __name__ == '__main__':

    underlying_price = 31  # index level
    strike = 30  # option_valuation strike
    maturity = 0.75  # maturity date
    r = 0.05  # risk-less short rate
    volatility = 0.3  # volatility
    n = 3 #Steps
    style = 1
    asset = 4
    type = 2

    marketData = MarketData(r, volatility)
    stock_option = BinaryOption(type, style, underlying_price, strike, maturity, volatility, asset,marketData, 4)

    print(stock_option)
    print(stock_option.getUp())
    print(stock_option.getDown())
    print(stock_option.riskNeutralProbability())

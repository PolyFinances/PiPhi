__author__ = "Sarah Souissi"
from option.binomial.binomial_option import BinaryOption
import matplotlib.pyplot as plt
import math
from option.market_data import MarketData

class BinaryTree():

    def __init__(self, i,option=None,parent=None):
        self.parent = parent
        self.upTree = None
        self.downTree = None
        self.option = option
        self.drawPosition = (0,i)
        self.i = i
        self.St = option.underlying_price
        self.exercice = False


    def setPrice(self, St):
         self.St = St

    def getUpChild(self):
        return self.upTree

    def getDownChild(self):
        return self.downTree

    def getRoot(self):
        node = self
        while node.parent != None:
            node = node.parent
        return node

    def getOption(self):
        root = self.getRoot()
        return root.option


    def insertDownTree(self, newNode):
        newNode.St = self.St * self.option.getDown()
        self.downTree = newNode
        self.downTree.parent = self
        #self.St = option.S0


    def insertUpTree(self,newNode):
        newNode.St = self.St * self.option.getUp()
        self.upTree = newNode
        self.upTree.parent = self

    def isDownChild(self):
        return self.parent.downTree == self

    def isUpChild(self):
        return self.parent.upTree == self

    def chemin(self):
        return


    def nbChildren(self):
        node = self
        nbchild = 0

        if node.downTree != None:
            nbchild += 1 + node.downTree.nbChildren()
        if node.upTree != None:
            nbchild += 1 + node.upTree.nbChildren()
        return nbchild

    def isLeaf(self):
        return self.getDownChild() == None and self.getUpChild()==None

    def isRoot(self):
        return self.getParent() == None

    def getParent(self):
        return self.parent

    def __repr__(self):
        #if (self != None):
        #    return str(self.i)
        return str(self.i)+" "+str(self.St) +" " + str(self.drawPosition)


def createTr(i, root):
    #print(i)
    if i > 0:
        root.insertDownTree(createTr(i-1, BinaryTree(i-1,root.getDown(),root)))
        root.insertUpTree(createTr(i-1,root.getDown(), BinaryTree(i-1, root.getUp(),root)))
    return root

def createTree(i, option):
    if i == 0:
        return BinaryTree(i,option)
    else:
        r =  BinaryTree(i,option)
        r.insertDownTree(createTree(i-1, option))
        r.insertUpTree(createTree(i-1, option))
        return r

def computeSt(tree, option, n):
    if tree!= None:
        if (tree.isRoot()) :
            tree.St = option.underlying_price
            tree.drawPosition =(0, (n+1)*10)

        elif tree.isDownChild():
            #print( tree.St + " " +str(tree.parent.St) + " " + str(option.getDown()))
            tree.St = tree.parent.St * option.getDown()
            #print( str(tree.St) + " " +str(tree.parent.St) + " " + str(option.getDown()))
            tree.drawPosition = (tree.parent.drawPosition[0]+10, tree.parent.drawPosition[1]-10)

        elif tree.isUpChild():
            tree.St =  tree.parent.St * option.getUp()
            #print(str( tree.St ) + " "+str(tree.parent.St) + " " + str(option.getUp()))
            tree.drawPosition = (tree.parent.drawPosition[0]+10,tree.parent.drawPosition[1]+10)
        computeSt(tree.getDownChild(), option, n)
        computeSt(tree.getUpChild(), option, n)


def computePayOff(tree, option, n):
    if tree.isLeaf():

        tree.payOff = option.payOff(tree.St)
        if tree.payOff  > 0 :
            tree.exercice = True
        return tree.payOff
    else:
        p = option.riskNeutralProbability()
        fd = computePayOff(tree.getDownChild(), option,n)
        fu = computePayOff(tree.getUpChild(), option,n)
        payOffBinomal = math.exp(-option.market_data.r*option.maturity/n)*(p*fu+(1-p)*fd)
        if option.style == 2 :
            pay_off_american_option = option.payOff(tree.St)
            if pay_off_american_option > payOffBinomal :
                #option exerciced
                tree.exercice = True
                tree.payOff = pay_off_american_option
            else :
                tree.payOff = payOffBinomal
        else :
            tree.payOff = payOffBinomal
        return tree.payOff


def plot(tree):
    edges = []
    if not tree.isLeaf():

        edges.append([tree.drawPosition, tree.getDownChild().drawPosition])
        edges.append([tree.drawPosition, tree.getUpChild().drawPosition])
        if tree.getDownChild() != None and tree.getUpChild() != None:
            edges = edges+plot(tree.getDownChild())
            edges = edges+plot(tree.getUpChild())
            #for e in plot(tree.getDownChild()):
            #    edges.append(e)
            #for e in plot(tree.getUpChild()):
            #    edges.append(e)
    return edges

def nodePositions(tree):
    position = set()
    #if tree.exercice == True
    position.add(((tree.drawPosition[0],tree.drawPosition[1]-4), tree.St, tree.payOff, tree.exercice))
    if tree.getDownChild() != None and tree.getUpChild() != None:
        for p in nodePositions(tree.getDownChild()):
            position.add(p)
        for p in nodePositions(tree.getUpChild()):
            position.add(p)
        #position.union(nodePositions(tree.getDownChild()))
        #position.union(nodePositions(tree.getUpChild()))
    return  position



if __name__ == '__main__':
    #myTree = BinaryTree("root")
    #myTree.insertDown(BinaryTree("downTree"))
    #myTree.insertUp(BinaryTree("upTree"))

    #print(myTree)
    #print(myTree.nbChildren())

    #myTree2 = BinaryTree("root")
    #createTree(myTree2, 4)
    #print(myTree2)
    #print(myTree2.nbChildren())

    #print(myTree2)
    #print(myTree2.nbChildren())
    #print(myTree2.profondeur())
    #node = myTree
    underlying_price = 31  # index level
    strike = 30  # option_valuation strike
    maturity = 0.75  # maturity date
    r = 0.05  # risk-less short rate
    volatility = 0.3  # volatility
    n = 3 #Steps
    style = 1
    asset = 4
    type = 2
    #str_K = input("Strike K (default Value "+str(K)+"): ")
    #if (str_K != "") :
    #    K = float(str_K)

    #str_S0 = input("Price S0 (default Value "+str(S0)+"): ")
    #if (str_S0 != "") :
    #    S0 = float(str_S0)

    #str_T = input("Maturity (in Years) (default Value "+str(T)+"): ")
    #if (str_T != "") :
    #    T = float(str_T)


    #str_r = input("Risk-less short rate r (default Value "+str(r)+"): ")
    #if (str_r != "") :
    #    r = float(str_r)

    #str_sigma = input("Volatility sigma(default Value "+str(sigma)+"): ")
    #if (str_sigma != "") :
    #    sigma = float(str_sigma)

    #str_n = input("Steps (Default Value "+str(n)+"): ")
    #if (str_n != "") :
    #    n = int(str_n)

    #str_style = input("style (Default Value 1): [1: Europeen, 2: American] ")
    #if (str_style != "") :
    #    style = int(str_style)

    #str_type = input("Type (Default Value 1):   [1: Call, 2: Put]")
    #if (str_type != "") :
    #    type = int(str_type)

    #str_asset = input("Asset [0: Equity , 1: Bond , 2 :Equity  paying dividends ,"
    #                  "3: Index ,  4: Future  ,5: Commodity , "
    #                  "6: Currency]  (Default Value"+ str(asset)+"): ")

    #if (str_asset != "") :
    #    asset = int(str_asset)

#    option = Option(S0, strike, maturity, r, volatility, n, style, type, asset)

    marketData = MarketData(r, volatility)
    option = BinaryOption(type, style, underlying_price, strike, maturity, volatility, asset,marketData, 4)

    #print(option)
    #root = BinaryTree(n,1, None ,option)
    #myTree2 = createTr(n,root)
    #print(myTree2)
    #node = myTree2
    #while node != None:
    #    print(node.hauteur())
    #    node = node.getDownChild()
    #    print(node)

    root = createTree(n, option)
    computeSt(root, option, n)
    print(computePayOff(root,option,n))
    #print(nodePositions(root))
    c = plot(root)

    fig = plt.figure()
    ax = fig.add_subplot(111)
    fig.subplots_adjust(top=0.85)

    noeuds = nodePositions(root)
    #plt.plot([-10,1], [-10,1], marker="^", color="black", markersize=10, label="iii")
    for l in c:
        #print(l)
        d = [[p[0] for p in l], [p[1] for p in l]]
        #print(str(d[0])+""+str( d[1]))
        ax.plot(d[0], d[1], 'k-*')
        #print (str(d[0]) +" " + str(d[1]) +"d[0]")
        #for p in l:
        #   noeuds.add(p)




    for p in noeuds:
        if p[3] == True:
            ax.annotate(str(round(p[1],2))+"\n\nPayOff="+str(round(p[2],2)), xy=p[0], arrowprops=dict(facecolor='black'), label="ss")
        # print(p[0])
        else :
            ax.annotate(str(round(p[1],2))+"\n\nPayOff="+str(round(p[2],2)), xy=p[0], label="")
        #ax.annotate(str(round(p[1],2)), xy=p[0])


    ax.annotate("should exercice the option", xy=(2, n*20+15), arrowprops=dict(facecolor='black'))

    #ax.legend()


    plt.title("Option Valuation \n" + str(option),  fontsize=9, fontweight='bold')


    plt.xlim([0, (n+1)*10])
    plt.ylim([0, (n+1)*20])
    plt.show()
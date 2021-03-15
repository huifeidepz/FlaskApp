import sys


from source.Tool.StoredProcedure import StoredPd

sys.path.append("..")
from source.DataAnalysis.ProductModel import ProductModel
from source.Spider.run import run


def StartSpider():

    run()


def StartTrainModel():
    pm = ProductModel()
    pm.GetPosOrNeg()
    pm.TrainModel()


if __name__ == '__main__':
    stp = StoredPd()

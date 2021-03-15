# -*- coding:utf8 -*-
import sys
from shutil import copyfile

sys.path.append("..")
from snownlp import SnowNLP
from snownlp import sentiment
from source.Tool.StoredProcedure import StoredPd


class ProductModel():
    def __init__(self):
        self.StoredPd = StoredPd()

    def GetPosOrNeg(self):
        print("Begin PosOrNeg")
        # 保存情感极性值小于等于0.3的结果为负面情感结果
        f1 = open('../../static/neg.txt', 'a+', encoding='utf-8')

        # 保存情感极性值大于0.3的结果为正面情感结果
        f2 = open('../../static/pos.txt', 'a+', encoding='utf-8')
        Contents = self.StoredPd.GetAllComments()
        print(len(Contents))
        num = 0
        for Content in Contents:
            num = num + 1
            s = SnowNLP(Content[1])
            result = s.sentiments
            self.StoredPd.UpdatePosOrNeg(Content[0], result)
            if result <= 0.4:
                f1.write(str(Content[1]) + '\n')
            else:
                f2.write(str(Content[1]) + '\n')
            if num % 100 == 0:
                print(num)
        f1.close()
        f2.close()

    def TrainModel(self):
        print("Begin Train Model")
        sentiment.train("../../static/neg.txt", "../../static/pos.txt")
        sentiment.save("../../static/sentiment.marshal")
        print("End Train Model")

    def DataStatistics(self):
        Data = self.StoredPd.GetDataGroupByBar()
        for data in Data:
            self.StoredPd.UpdatePostBar(data)
    # text = u'''
    # 小朋友不要骂人，叔叔说的是现实，天天往手机游戏或电脑里面充钱，你们这些钱是不是天天向父母身上要？'''
    # s = SnowNLP(text)  # 不只是情感分析，训练出的snownlp模型还有提取关键字，摘要等功能
    # print(s.words)
    # print(s.sentiments)
    # print(s.keywords(4))
    # print(s.summary(4))

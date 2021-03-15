# -*- coding:utf8 -*-
import sys

sys.path.append("..")
import operator

from source.Tool.StoredProcedure import StoredPd


class AnalsisPostBar(object):

    def __init__(self):
        self.StorePd = StoredPd()

    def AnalsisPosOrNeg(self, PostbarID):  # 情绪分析
        Datas = self.StorePd.GetCommetPosOrNegbyPostBar(PostbarID)

        datas = []
        rows = []
        for i in range(len(Datas)):
            st = Datas[i][0]
            datas.append(st[0:3])
        dataSet = set(datas)
        BigPosNeg = 0
        for dataset in dataSet:
            if dataset < str(1):
                array = {"PosOrNeg": dataset, "Num": datas.count(dataset)}
                rows.append(array)
            else:
                BigPosNeg += datas.count(dataset)
        array = {"PosOrNeg": str(1), "Num": BigPosNeg}
        rows.append(array)
        return sorted(rows, key=operator.itemgetter("PosOrNeg"))

    def AnalsisUserByLevel(self, PostbarID):  # 分析用户等级
        Data = self.StorePd.GetPostBarUserByLevel(PostbarID)

        rows = []
        for data in Data:
            row = {"UserLevel": data[0], "Num": data[1]}
            rows.append(row)
        return rows

    def AnalsisUserBytime(self):  # 分析用户活跃时间
        pass

    def AnalsisWordCloud(self):  # 分析词频
        pass

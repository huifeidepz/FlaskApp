import threading
import unittest
import sys
from shutil import copyfile

from source.DataAnalysis.ProductModel import ProductModel
from source.Starter.Start import StartSpider
from source.Tool import Common
from source.Tool.StoredProcedure import StoredPd
from source.Tool.Mysqlpool import Mysql_Pool
from source.Tool.RedisPro import RedisControl

stp = StoredPd()
RC = RedisControl()


class MyTestCase(unittest.TestCase):
    def test_something(self):
        PostBars = stp.GetAllPostBar()
        data = {"columns": ['PostBarID', 'TotalPage', 'TotalComment'], "rows": []}
        for PostBar in PostBars:
            Total = stp.GetAllPostBarTotal(PostBar[0])
            row = {
                "PostBarID": PostBar[0],
                "TotalPage": Total[0],
                "TotalComment": Total[1]
            }
            data["rows"].append(row)
        print(data)

    def testAnalysis(self):
        se = Common.getSelector("https://tieba.baidu.com/p/115348887")
        print(se.xpath(
            '//*[@id="thread_theme_5"]/div[1]/ul/li[1]/a[text()="下一页"]/@href'))

    def test(self):
        # ss = StartSpider()
        # if ss.flag == 0:
        #     t = threading.Thread(ss.StartSpider())
        #     t.start()
        # return ss.flag
        # RC.setData("SpiderFlag", "0")
        # RC.setData("TrainModelFlag", "0")
        # RC.setData("wp7", "1")
        # print(RC.getData("wp7"))
        # print(len(stp.GetAllComments()))
        PostBarID = '印度'
        # request.values.get(" PostBar")
        # url = "https://tieba.baidu.com/f?kw={}".format(PostBarID)
        # re = Common.getRespon(url)
        ProductModel().DataStatistics()
        # print(stp.insertPostBar(PostBarID))



if __name__ == '__main__':
    unittest.main()

# -*- coding:utf8 -*-
import os
import sys

sys.path.append("..")

def run():
    #import subprocess
    ## 方法1
    sys.path.append(os.path.dirname(os.path.realpath(__file__)))
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    print(os.getcwd())
    os.system('scrapy crawl PostSpider')
    #subprocess.check_call('scrapy crawl PostSpider', cwd='source/Spider')
    # os.system("cd source\Spider")
    # print(os.getcwd())
    #
    # os.system("scrapy crawl PostSpider")


if __name__ == '__main__':
    run()

# -*- coding:utf-8 -*-
# @Filename : 24.py 
# @Author : Lizi
# @Time : 2020/3/9 16:57 
# @Software: PyCharm

import pysnooper
from decimal import Decimal

scala = 1000
ListPriceList= [(0.01,0.25,0.001),(0.25,0.5,0.005),(0.5,10,0.01),
                (10,20,0.02),(20,100,0.05),(100,200,0.1),(200,500,0.2),
                (500,1000,0.5),(1000,2000,1),(2000,5000,2),(5000,9995,5)]


def Spread(lastprice):
    lastprice*=scala
    for item in ListPriceList:
        if lastprice / scala < 0.01 or lastprice / scala >= 9995:
            print("获取不到 " + str(lastprice / scala) + "的所在区间")
            if lastprice % scala == 0.0:
                position = ListPriceList.index(item)
                preposition = 0 if position - 1<0 else position -1
                nextposition = 10 if position + 1>0 else position+1
                print("最小价格变动值" + str(item[2]))
                return (ListPriceList(preposition),ListPriceList(preposition),ListPriceList(nextposition))
            else:
                print("最小价格变动值" + str(item[2]))
                print(str(lastprice/scala) + "不是" + str(item) + "的整数倍")



if __name__ == "__main__":
    LastPrice = float(input("请输入最新价："))
    zone=Spread(LastPrice)
    print(zone)
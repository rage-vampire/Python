# -*- coding:utf-8 -*-
# Filename: 24spread.py
# Author: Lizi
# Time: 2019/12/20 13:58

# 计算港股24价差

import pysnooper
from decimal import Decimal

scala = 1000
# LastPrice = 0
# 将每个区间和最小价位差以列表的方式存储
ListPriceList = [(0.01, 0.25, 0.001), (0.25, 0.5, 0.005), (0.5, 10, 0.01),
                 (10, 20, 0.02), (20, 100, 0.05), (100, 200, 0.1), (200, 500, 0.2),
                 (500, 1000, 0.5), (1000, 2000, 1), (2000, 5000, 2), (5000, 9995, 5)]


# 获取最新价所在区间
# active = True
# while active:
# @pysnooper.snoop('log/file.log')
@pysnooper.snoop('log/file.log', prefix='Spread:')
def Spread(lastPrice):
    lastPrice *= scala
    if lastPrice / scala < 0.01 or lastPrice / scala >= 9995:
        print("获取不到 " + str(lastPrice / scala) + " 所在区间")
    for item in ListPriceList:  # 遍历列表中的项
        if item[0] * scala <= lastPrice < item[1] * scala:  # 判断最新价是否大于等于左边界，且小于右边界。通过item[0]、item[1]、item[2]的索引获取左右边界的值，以及最小变动差
            if lastPrice % (item[2] * scala) == 0.0:  # 判断最新价是否能被最小价位整除
                position = ListPriceList.index(item)  # 获取最新价所在的当前区间
                prePosition = 0 if position - 1 < 0 else position - 1  # 获取最新价前一个区间
                nextPosition = 10 if position + 1 > 10 else position + 1  # 获取最新价后一个区间
                print("最小变动价格为: " + str(item[2]))
                return ListPriceList[prePosition], item, ListPriceList[nextPosition]  # 返回三个区间的值，方便后面的函数调用
            else:
                print("最小变动价格为: " + str(item[2]))
                print("余数为：" + str(lastPrice % (item[2] * scala)))
                print(str(lastPrice / scala) + " 不是最小变动价格 " + str(item[2]) + " 的整数倍 ")
                return None  # last price is error,不是item区间的最小变动价的整数倍


# 计算下限值
# @pysnooper.snoop('log/file.log')
@pysnooper.snoop('log/file.log', prefix='MinLimit:')
def MinLimit(lastprice, MinPriceValue1, MinPriceValue, leftvalue, rightvalue):
    CurrentPrice = 0
    if lastprice == 0.01 or lastprice - 24 * MinPriceValue <= 0.01:
        CurrentPrice = 0.01

    elif lastprice == leftvalue:
        CurrentPrice = Decimal(lastprice - 24 * MinPriceValue1).quantize(Decimal("0.0000"))

    elif lastprice > leftvalue > lastprice - 24 * MinPriceValue:
        CurrentPrice = Decimal(leftvalue - (24 - (lastprice - leftvalue) / MinPriceValue) * MinPriceValue1).quantize(
            Decimal("0.0000"))

    elif lastprice > leftvalue and leftvalue <= lastprice - 24 * MinPriceValue <= rightvalue:
        CurrentPrice = Decimal(lastprice - 24 * MinPriceValue).quantize(Decimal("0.0000"))
    print("24价差下限值为: " + str(CurrentPrice))


# 计算24上限值
# @pysnooper.snoop('log/file.log')
@pysnooper.snoop('log/file.log', prefix='MaxLimit:')
def MaxLimit(lastprice, MinPriceValue, MinPriceValue2, rightvalue):
    CurrentPrice = 0
    if Decimal(lastprice + 24 * MinPriceValue).quantize(Decimal("0.0000")) <= Decimal(rightvalue).quantize(
            Decimal("0.0000")):
        CurrentPrice = Decimal(lastprice + 24 * MinPriceValue).quantize(Decimal("0.0000"))

    elif Decimal(lastprice + 24 * MinPriceValue).quantize(Decimal("0.0000")) > Decimal(rightvalue).quantize(
            Decimal("0.0000")):
        CurrentPrice = Decimal(rightvalue + (24 - (rightvalue - lastprice) / MinPriceValue) * MinPriceValue2).quantize(
            Decimal("0.0000"))
    print("24价差上限值为: " + str(CurrentPrice))


if __name__ == "__main__":
    active = True
    while active:
        LastPrice = float(input("请输入最新价LastPrice: "))
        zone = Spread(LastPrice)  # 调用Spread函数
        print(zone)  # 将Spread函数的返回值打印出来
        if zone is not None:
            Minprice = MinLimit(LastPrice, zone[0][2], zone[1][2], zone[1][0],zone[1][1])  # 将Spread函数返回的值传给MinLimit函数的参数，通过zone[X][Y]获取对应区间，以及对应区间的左右边界值和最小价位差
            MaxPrice = MaxLimit(LastPrice, zone[1][2], zone[2][2], zone[1][1])
        if LastPrice == 0:
            break

    # if LastPrice == 0:
    #     break

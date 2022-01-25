# -*- coding:utf-8 -*-
# @Filename : test45.py 
# @Author : Lizi
# @Time : 2020/3/25 21:58 
# @Software: PyCharm

import os
from decimal import Decimal
from decimal import DecimalException
import pprint


def readname():
    filepath = 'D:\电子发票'
    name = os.listdir(filepath)
    return name


sum1 = 0
count = 0
if __name__ == '__main__':
    name = readname()
    pprint.pprint(name)
    try:
        for i, v in enumerate(name):
            print((v.rstrip('.pdf')))
            count += 1
            sum0 = Decimal(v.rstrip('.pdf')).quantize(Decimal("0.000"))
            sum1 += sum0
    except DecimalException as e:
        print("出现异常，请检查:{}".format(e))
    else:
        print("共有:{}张发票".format(count))
        print("发票总金额为：{}元".format(sum1))
    finally:
        print('Cleaning up....')
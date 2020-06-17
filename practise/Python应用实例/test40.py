# -*- coding:utf-8 -*-
# @Filename : test40.py 
# @Author : Lizi
# @Time : 2020/3/16 21:00 
# @Software: PyCharm

import random
from random import randint
from random import choice
random.seed(5)

# # 递归一：n的阶乘
# def fac(n):
#     if n == 1:
#         return n
#     else:
#         return n * fac(n-1)
#
# if __name__ == "__main__":
#     number = int(input("请输入n的值："))
#     num = fac(number)
#     print (str(number) + "的阶乘为" + str(num) )


# # 递归二：幂运算
# # 1、对于任何数值X，power（x，0）都为1
# # 2、n>0，power(x,n)为power(x,n-1)与x的乘积
# def pow(x,n):
#     if n == 0:
#         return 1
#     else:
#         return x * pow(x,n-1)
#
# if __name__ == "__main__":
#     num1 = int(input("请输入X的值："))
#     num2 = int(input("请输入n的值："))
#     num = pow(num1,num2)
#     print(str(num1) + "的" + str(num2) +"次方为：{}".format(num) )

# # 递归二：二分法查找
def search(sequence,number,lower=0,upper=None):
    if upper is None:
        upper = len(sequence)-1
    if lower == upper:
        assert number == sequence[upper]
        return upper
    else:
        middle = (lower+upper) // 2
        if number > sequence[middle]:
            return search(sequence,number,middle+1,upper)
        else:
            return search(sequence,number,lower,middle)

if __name__ == "__mian__":
    seq = [45,20,85,40,125,30,95]
    num = search(seq.sort(),34)
    print(num)
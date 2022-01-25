# -*- coding: UTF-8 -*-
# 斐波那契数列
import math

def fibs(num):
    '斐波那契数列'
    fib = [0, 1]
    for i in range(num):
        fib.append(fib[-2]+fib[-1])
    return fib

if __name__=="__main__":
    num = int(input("please enter num : "))
    #fib = fibs(num)
    print (fibs(num))

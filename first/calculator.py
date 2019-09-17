# -*- coding: utf-8 -*-
# @file   : calculator.py
# @author : lizi
# @date   : 2019/9/17
# @version: 1.0
# @desc   :

#相加
def add(x,y):
    return x + y
#相减
def subtract(x,y):
    return x - y
#相乘
def multiply(x,y):
    return x * y
#相除
def divide(x,y):
    return x / y
if __name__ == '__main__':
    num1 = int(input("Please enter the first num1:"))
    num2 = int(input("Please enter the second num2:"))
    print("Please enter your operator：")
    print("+:add")
    print("-:subtract")
    print("*:multiply")
    print("/:divide")
    choice = input("Please enter your choice(+、-、*、/):")
    if choice == '+':
        print(num1,'+',num2,'=',add(num1,num2))
    elif choice == '-':
        print(num1,'-',num2,'=',subtract(num1,num2))
    elif choice == '*':
        print(num1,'*',num2,'=',multiply(num1,num2))
    # try except ZeroDivisionError模块避免除数为0，抛异常
    elif choice == '/':
        try:
            print(num1, '/', num2, '=', divide(num1, num2))
        except ZeroDivisionError:
            print("You can not divide by 0!")
    else:
        print("非法输入!")
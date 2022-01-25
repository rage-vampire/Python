# -*- coding:utf-8 -*-
# @Filename : test41.py 
# @Author : Lizi
# @Time : 2020/3/21 15:14 
# @Software: PyCharm


while True:
    try:
        x = int(input("please enter X : "))
        y = int(input("Please enter Y : "))
        print(x/y)
    except Exception as e:
        print(e)
        print("please try again!")
    else:
        break
    finally:
        print("please clean up......")

# # x = None
# try:
#     x = int(input("please enter X : "))
#     y = int(input("Please enter Y : "))
#     print(x / y)
# finally:
#     print('clean up ....')
#     del x


# -*- coding:utf-8 -*-
# @Filename : zhishu.py 
# @Author : Lizi
# @Time : 2020/6/22 14:21 
# @Software: PyCharm

'''一个大于1的自然数，除了1和它本身外，不能被其他自然数（质数）整除（2, 3, 5, 7等），换句话说就是该数除了1和它本身以外不再有其他的因数。'''

def is_zhishu(num):
    if num > 1:
        for i in range(2,num):
            if num % i == 0:
                print(num, '不是质数')
                print(i, '乘于', num // i, '等于', num)
                break
        else:
            print(num, '是质数')
    else:
        print(num, '不是质数')


'''输出指定范围内的质数'''
def rang_zhishu(lower,upper):
    for num in range(lower, upper+1):
        if num > 1:
            for i in range(2,num):
                if num % i == 0:
                    # print(num, '不是质数')
                    break
            else:
                print('质数有：', num)


if __name__ == '__main__':
    is_zhishu(8)
    rang_zhishu(1,100)
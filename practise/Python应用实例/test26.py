"""
古典问题：有一对兔子，从出生后第3个月起每个月都生一对兔子，小兔子长到第三个月
后每个月又生一对兔子，假如兔子都不死，问每个月的兔子总数为多少？
斐波那契数列。
程序分析：斐波那契数列（Fibonacci sequence），又称黄金分割数列，
指的是这样一个数列：0、1、1、2、3、5、8、13、21、34、……。
在数学上，费波那契数列是以递归的方法来定义：
思路 ：1 1 2 3 5 8 13。。。以此类推
"""
count = 1
list_total = []
for i in range(1,13):
    if i < 3:
        total = 1
        print('第{0}个月兔子量为：{1}'.format(i,total))
        list_total.append(total)
    else:
        total = list_total[i-2] + list_total[i-3]
        list_total.append(total)
        print('第{0}个月兔子量为：{1}'.format(i, total))




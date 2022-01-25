#14、python中生成随机整数、随机小数、0--1之间小数方法
'''
随机整数：random.randint(a,b),生成区间内的整数
随机小数：习惯用numpy库，利用np.random.randn(5)生成5个随机小数
0-1随机小数：random.random(),括号中不传参
'''
import random
import numpy
#随机整数
result = random.randint(10,20)
#随机小数
res = numpy.random.randn(5)
#0-1的随机小数
ret = random.random()

print(result)
print(res)
print(ret)



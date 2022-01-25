# 要求：合并成{"A":1,"B":2,"C":3},请用一行代码实现

#zip() 函数用于将可迭代的对象作为参数，将对象中对应的元素打包成一个个元组，然后返回由这些元组组成的列表。
keys = ["A","B","C"]
values = [1,2,3]

dict_1= dict(zip(keys,values))
#dict_2 = {i:j for i,j in zip(keys,values)}
print(dict_1)
#print(dict_2)
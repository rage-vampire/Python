#8、a) //等长的两个列表合并到一个字典，要求：合并成{"A":1,"B":2,"C":3},请用一行代码实现
keys = ["A","B","C"]
values = ["1","2","3"]
print(dict(zip(keys,[int(x) for x in values])))

#b)//合并两个列表并消除重复值
list_1 = ["a","b","c","1","A","winning"]
list_2 = ["a","python","string","1"]
print(set(list_1 + list_2))

#c) //已知一个列表，根据字典中的x，由大到小排序这个列表
a = [{"x":1,"y":2},{"x":2,"y":3},{"x":3,"y":4}]

print(sorted(a,key=lambda item:item["x"],reverse=True))

#s = "ajldjlajfdljfddd"，去重并从小到大排序输出"adfjl"
s = 'fafafdshghfdhghg'
s = set(s)
s = list(s)
s.sort()
print(s)
res = "".join(s)
print(res)

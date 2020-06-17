#列表[1,2,3,4,5],请使用map()函数输出[1,4,9,16,25]，
# 并使用列表推导式提取出大于10的数，最终输出[16,25]
list = [1,2,3,4,5]
def fn(x):
    return x**2
res = map(fn,list)
res = [i for i in res if i > 0]
print(res)
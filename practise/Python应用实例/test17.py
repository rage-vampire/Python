# 40、x="abc",y="def",z=["d","e","f"],分别求出x.join(y)和x.join(z)返回的结果
# join()括号里面的是可迭代对象，x插入可迭代对象中间，形成字符串，结果一致，有没有突然感觉字符串的常见操作都不会玩了
# 顺便建议大家学下os.path.join()方法，拼接路径经常用到，
# 也用到了join,和字符串操作中的join有什么区别，该问题大家可以查阅相关文档，后期会有答案

x = 'abc'
y = 'def'
d = ['d','e','f']

m = x.join(y)
n = x.join(d)
print(m)
print(n)
#输出结果
# dabceabcf
# dabceabcf


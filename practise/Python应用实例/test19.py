#一球从100米高度自由落下，每次落地后反跳回原高度的一半；再落下，求它在
# 第10次落地时，共经过多少米？第10次反弹多高？
height = 100
lognth = 100
for i in range(1,11):
    if i != 1:
        lognth = lognth + height*2
    else:
        lognth = 100
    height = height / 2
    print('第'+str(i)+'次高度为：'+str(height))
    print('经过高度为:'+str(lognth))

print(height)
print(lognth)




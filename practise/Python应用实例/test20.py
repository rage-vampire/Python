#有1、2、3、4个数字，能组成多少个互不相同且无重复数字的三位数？都是多少？
a = 0
for i in range(1,5):
    for j in range(1,5):
        for k in range(1,5):
            if( i != k ) and (i != j) and (j != k):
                a = a+1
                print(i,j,k)
print("一共有" + str(a) +'种')

#将一个正整数分解质因数。例如：输入90,打印出90=2*3*3*5。
from sys import stdout
n = int(input('请输入一个整数:'))
# print ("n = %d" % n)
# for i in range(2,n + 1):
#     while n != i:
#         if n % i == 0:
#             stdout.write(str(i))
#             stdout.write("*")
#             n = n / i
#         else:
#             break
# print ("%d" % n)
count = n+1
list_a = []
for i in range(2,count):
    while  n > i:
        if n % i == 0:
            list_a.append(i)
            n = int(n/i)
        else:
            break
list_a.append(n)
print(list_a)


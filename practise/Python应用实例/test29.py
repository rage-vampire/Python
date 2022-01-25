#求s=a+aa+aaa+aaaa+aa...a的值，其中a是一个数字。例如2+22+222+2222+22222(此时
#共有5个数相加)，几个数相加有键盘控制。
a = int(input('请输入一个10以内的非零整数：'))
n = int(input('请输入累加次数：'))
b = a
list_a = [a]
c = 0
for i in range(1,n+1):
    b = (10**i)*a + b
    list_a.append(b)
for i in range(n+1):
   c = list_a[i] + c

print(c)


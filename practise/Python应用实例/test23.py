#输入三个整数x,y,z，请把这三个数由小到大输出。
list_a = []
for i in range(1,4):
    a = input('清楚输入第{0}个数字：'.format(i))
    list_a.append(a)
list_b = sorted(list_a)
for j in list_b:
    print(j)


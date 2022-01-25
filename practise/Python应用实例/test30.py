#10000以内的数字等于约数之和 如6=1+2+3
list_all = []
for i in range(1,10001):
    sum_add = 0
    for j in range(1,i):
        if i % j ==0:
            sum_add += j
    if sum_add == i:
        list_all.append(i)

print(list_all)


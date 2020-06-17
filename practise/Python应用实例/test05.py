#判断101-200之间有多少个素数，并输出所有素数。
num_list = []
for i in range(101,201):
    num_list.append(i)

for i in range(101,201):
    for j in range(2,i):
        if i%j ==0:
            num_list.remove(i)
            break
print(num_list)




list = []
for i in range(1,10):
    for j in range(1,i+1):
        a = str(j)+'*'+str(i)+'='+str(i*j)
        list.append(a)
    print(' '.join(list))
    list = []



for i in range(1,10):
    for j in range(1,i+1):
        print("{}*{}={}\t".format(j,i,i*j),end="")
    print()

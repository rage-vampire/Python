def f(x,l=[]):
    for i in range(x):
        l.append(i*i)
    print(l)

f(3)
f(3,[3,2,1])
f(3)
count=0
for i in range(1,101):
    if i%3==0 or i%5==0:
        print(i,end=' ')
        count+=1
        if count==8:
            print('\n')
            count=0

list_a = ['a','a','a','a','a','a','a','a','a']
while len(list_a)>4:
    for i in range(1,7):
        if i == 6:
            list_a.pop(-1)
print(list_a)

def aa(val,list=[]):
    list.append(val)
    return list

list1 = aa(10)
list2 = aa(123,[])
list3 = aa('a')
print(list1)
print(list2)
print(list3)
'''
输出结果：
[10, 'a']
[123]
[10, 'a']
'''

list_2 = [[]]*5
list_2[0].append(10)
print(list_2)
list_2[1].append(20)
print(list_2)
list_2.append(30)
print(list_2)
'''
输出结果：
[[10], [10], [10], [10], [10]]
[[10, 20], [10, 20], [10, 20], [10, 20], [10, 20]]
[[10, 20], [10, 20], [10, 20], [10, 20], [10, 20], 30]
'''





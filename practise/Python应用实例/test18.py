#44、列表去重

#方法1：不改变原始列表序列
a = [1,4,4,6,7,3,4,3,4]

new_list = []
for i in a:
    if i not in new_list:
        new_list.append(i)

print(new_list)

#方法2：改编原始列表序列

b = [1,4,4,6,7,3,4,3,4]

b = list(set(b))
print(b)
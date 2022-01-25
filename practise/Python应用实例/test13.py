#24、字典根据键从小到大排序dict={"name":"zs","age":18,"city":"深圳","tel":"1362626627"}

dict={"name":"zs","age":18,"city":"深圳","tel":"1362626627"}
list = sorted(dict.items(),key=lambda i:i[0],reverse=False)
print(list)
new_dict = {}
for i in  list:
    new_dict[i[0]] = i[1]
print(new_dict)


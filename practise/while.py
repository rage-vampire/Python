# -*- coding:utf-8 -*-
# Filename: while.py
# Author: Lizi
# Time: 2019/12/20 15:51

# 在列表之间移动元素
# unconfirmed_users = ['alice','brian','candace']
# confirmed_users = []
# while unconfirmed_users:
#     currents = unconfirmed_users.pop()
#     print(currents.title())
#     confirmed_users.append(currents)
# print("\n已确认的用户:")
# for confirmed_user in confirmed_users:
#     print(confirmed_user.title())


# 删除包含特定值的所有元素
# num_list = [1,2,3,4,5,1,1,1,45,67,1,]
# while 1 in num_list:
#     num_list.remove(1)
# print(num_list)

# 使用用户输入来填充字典
responses = {}
active = True
while active:
    name = input("what is your name ? ")
    response = input("which mountai would you like to climb someday?")
    responses[name] = response

    repeat = input("would you like to let anther person respond (yes/no) ?")
    if repeat == 'no':
        active = False

for name,response in responses.items():
    print(name.title() + " would like to climb " + response.title() + ".")
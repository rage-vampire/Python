# -*- coding:utf-8 -*-
# Filename: def.py
# Author: Lizi
# Time: 2019/12/20 16:20

# 让实参变成可选的
# def get_name(first_name,last_name,middle_name=''):
#     full_name = [first_name.title() + " " + last_name]         # 返回列表类型
#     if middle_name:
#         full_name = {"first_name": first_name.title(), "middle_name":middle_name.title(),"last_name":last_name.title()}          #返回字典类型
#     return full_name
# name = get_name("zhang","san")
# print(name)
# name = get_name('john','hooker','lee')
# print(name)

# 结合使用函数和while循环
# def get_name(first_name,last_name):
#     full_name = first_name.title() + " " + last_name         # 返回列表类型
#     return full_name
#
# while True:
#     print("\nplease enter your name:")
#     print("please enter 'q' to quit!")
#     f_name = input("Firstname: ")
#     if f_name == 'q':
#         break
#     l_name = input("Lastname: ")
#     if l_name == 'q':
#         break
#     name = get_name(f_name,l_name)
#     print("Hello " + name)

# for char in "python string":
#     if char == " ":
#         break
#     print(char,end='')
#
#     if char == '0':
#         continue


# 使用任意数量的关键字参数
def build_profile(first,last,**user_info):              # **user_info表示创建一个空字典，*user_info表示空元祖
    profile = {}
    profile['firstname'] = first
    profile['lastname'] = last

    for key,value in user_info.items():
        profile[key]=value
    return profile
user_profile = build_profile('albert','alice',
              country = 'Amcian',age = 25)
print(user_profile)
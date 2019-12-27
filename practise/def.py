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
# def build_profile(first,last,**user_info):              # **user_info表示创建一个空字典，*user_info表示空元祖
#     profile = {}
#     profile['firstname'] = first
#     profile['lastname'] = last
#
#     for key,value in user_info.items():
#         profile[key]=value
#     return profile
# user_profile = build_profile('albert','alice',
#               country = 'Amcian',age = 25)
# print(user_profile)





# # 二、函数的递归
# # 求n的阶乘
# def factorial(n):
#     if n==1:
#         return 1
#     else:
#         return n * factorial(n-1)
#
# if __name__ == "__main__":
#     n = factorial(int(input("请输入n：")))
#     print(n)


# 二分法查找
# def search (sequence,number,lower=0,upper=None):
#     # if upper is None:
#     #     upper = len(sequence)-1
#     if lower == upper:
#         assert number == sequence[upper]
#         return upper
#     else:
#         middle = (lower+upper)//2
#         if number > sequence[middle]:
#             return search(sequence,number,middle+1,upper)
#         else:
#             return search(sequence,lower,number,middle)
#
# if __name__ =="__main__":
#     seq = [34,67,8,123,4,100,95]
#     seq.sort()
#     print(seq)
#     print(search(seq,34))


def d_sum(L):
    # 打印该层级L
    print(L)
    if not L:
        return 0
    else:
        return L[0] + d_sum(L[1:])

# 构建 0-10 数字元素列表
L = [i for i in range(100)]
sum_l = d_sum(L)
print(sum_l)
print(d_sum(L[1:]))
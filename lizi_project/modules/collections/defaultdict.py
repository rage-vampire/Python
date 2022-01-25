# -*- coding:utf-8 -*-
# @Filename : defaultdict.py 
# @Author : Lizi
# @Time : 2020/6/17 10:44 
# @Software: PyCharm


from collections import defaultdict


# dict_int = defaultdict(int)
# dict_str = defaultdict(str)
# dict_list = defaultdict(list)
# dict_tuple = defaultdict(tuple)
# dict_set = defaultdict(set)
#
# print("dict_int:", dict_int['键名'])
# print("dict_str:", dict_str['键名'])
# print("dict_list:", dict_list['键名'])
# print("dict_tuple:", dict_tuple['键名'])
# print("dict_set:", dict_set['键名'])
# dict_int["第二个值"] = [123124]
# print(dict_int)

strings = ('puppy', 'kitten', 'puppy', 'puppy','weasel', 'puppy', 'kitten', 'puppy')
counts = defaultdict(int)     # conuts为defaultdict类型的字典，
for kw in strings:
    # print(counts[kw])
    counts[kw] += 1    # counts[kw]：获取键的值，当键不存在是提供默认值0
print(counts)     # 输出一个键值对的字典，值为键出现的次数

"""使用list作第一个参数，可以很容易将键-值对序列转换为列表字典"""
# s = [('yellow', 1), ('blue', 2), ('yellow', 3), ('blue', 4), ('red', 1)]
# d = defaultdict(list)    # 默认返回一个列表
# for k, v in s:
#     d[k].append(v)
# print(sorted(d.items()))

s = [('red', 1), ('blue', 2), ('red', 3), ('blue', 4), ('red', 1), ('blue', 4)]
d = defaultdict(set)
for k, v in s:
    d[k].add(v)
print(d)
print(sorted(d.items()))



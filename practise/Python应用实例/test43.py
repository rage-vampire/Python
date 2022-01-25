# -*- coding:utf-8 -*-
# @Filename : test43.py 
# @Author : Lizi
# @Time : 2020/3/25 10:34 
# @Software: PyCharm

# def check_index(key):
#     if not isinstance(key, int):
#         raise TypeError
#     if key < 0:
#         raise IndexError
#
#
# class Sequence:
#
#     def __init__(self, start, step=1):
#         self.start1 = start
#         self.step1 = step
#         self.change = {}
#
#     def __getitem__(self, key):
#         check_index(key)
#         try:
#             return self.change[key]
#         except KeyError:
#             return self.start1 + self.step1 * key
#
#     def __setitem__(self, key, value):
#         check_index(key)
#         self.change[key] = value
#
#
# if __name__ == "__main__":
#     s = Sequence(1, 2)
#     print(s[4])
#     s[4] = 2
#     print(s[4])
# --------------------------------------------------------------------
#
# class Animal:
#     def __init__(self, animal_list):
#         self.animals_name = animal_list
#
#     def __getitem__(self, item):
#         return self.animals_name[item]
#
#
# animals = Animal(["dog", "cat", "fish"])
# for animal in animals:
#     print(animal)

# ------------------------------------------------------------------------


class CounterList(list):
    def __init__(self,*args):
        super().__init__(*args)
        self.count = 0

    def __getitem__(self, item):
        self.count += 1
        return super().__getitem__(item)
        # return super(CounterList,self).__getitem__(item)



cl = CounterList(range(10))
print(cl)
print(cl.count)
print(cl[4]+cl[2])
print(cl.count)
print(cl[4])
print(cl.count)
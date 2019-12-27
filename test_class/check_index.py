# # -*- coding:utf-8 -*-
# # Filename: check_index.py
# # Author: Lizi
# # Time: 2019/12/24 10:15
#
#
# class Mylist():
#     def __init__(self,*args):
#         for x in args:
#             self.values = x
#             self.count = {}.fromkeys(range(len(self.values)),0)
#
#     def __len__(self):
#         return len(self.values)
#
#     def __getitem__(self, value):
#         self.count[value] += 1
#         return self.values[value]
#
# if __name__ == "__main__":
#     test = Mylist(range(11))
#     print(test.count)
#     print(len(test))
#     test.count[0] = 3
#     print(test.count)
#     print(test.values)


def aa(x):
    """ahfnwwfnwe"""
    return x*x
b=aa(2)
print(aa.__doc__)
help(aa)
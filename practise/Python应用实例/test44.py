# -*- coding:utf-8 -*-
# @Filename : test44.py 
# @Author : Lizi
# @Time : 2020/3/25 15:28 
# @Software: PyCharm


# class Rectangle:
#     def __init__(self,width,height):
#         self.width1 = width
#         self.height1 = height
#
#     def get_size(self):
#         return self.width1,self.height1
#
#     def set_size(self,size):
#         self.width1,self.height1 = size
#
#     sizenum = property(get_size,set_size)    #通过存取方法定义属性
#
#
# r = Rectangle(10,5)
# print(r.get_size())
# r.sizenum = 150
# print(r.width1)
# print(r.height1)

# --------------------------------------------------------
class Rectangle:
    def __init__(self,width,height):
        self.width1 = width
        self.height1 = height

    def __setattr__(self, key, value):
        if key == 'size':
            self.width1,self.height1 = value
        else:
            self.__dict__[key] = value

    def __getattr__(self, item):
        if item == "size":
            return self.width1,self.height1
        else:
            raise AttributeError


if __name__ == '__main__':
    size = Rectangle(20,30)
    print(size.width1)
    # print(s.height1)
    size.width1 = 50
    print(size.width1)


# --------------------------------------------------------
# class Person:
#
#     # @property
#     def get_name(self):
#         print('我叫xxx')
#
#
# if __name__ == '__main__':
#     person = Person()
#     person.get_name()

# --------------------------------------------------------

# class Person(object):
#     @property
#     def get_name(self):
#         print('我叫yyy')
#
#
# if __name__ == '__main__':
#     person = Person()
#     person.get_name
# --------------------------------------------------------

# class Goods:
#     @property
#     def price(self):
#         print("@property")
#     @price.setter
#     def price(self,value):
#         print("@price.setter:" + str(value))
#     @price.deleter
#     def price(self):
#         print("@price.deleter")
# obj = Goods()
# obj.price = 50
# print(obj.price)
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : dict_method.py
# @Author: Lizi
# @Date  : 2020/9/11


def dict_clear():
    """d.clear()删除字典中的项"""
    dict_1 = {
        "name": "yanglili",
        "age": 25,
        "sex": 'women',
        "tel": 1893889
    }

    dict_1.clear()
    print('清除后的字典：', dict_1)


def dict_copy():
    """d.copy(),浅复制，修改副本后，原件也被修改"""
    dict_1 = {
        "name": "yanglili",
        "age": 25,
        "sex": 'women',
        "tel": 1893889
    }

    dict_2 = dict_1.copy()
    dict_2["age"] = 28
    print("重新赋值后的字典：", dict_1, dict_2)


def dict_fromkeys():
    """dict.fromkeys(seq[, value])函数用于创建一个新字典，以序列 seq 中元素做字典的键，value 为字典所有键对应的初始值,值默认为None"""
    seq = ['a', 'b', 'c']
    dict_1 = dict.fromkeys(seq)
    dict_2 = dict.fromkeys(seq, 'python')
    print("fromkeys默认值为None：", dict_1)
    print("fromkeys指定值：", dict_2)


def dict_get():
    """dict.get(key, default=None) 函数返回指定键的值，如果键不在字典中返回默认值"""
    dict_1 = {
        "name": "yanglili",
        "age": 25,
        "sex": 'women',
        "tel": 1893889
    }
    dict_2 = {}
    print("get返回已有值yanglili:", dict_1.get('name'))
    print("get返回已有值yanglili:", dict_1.get('name', "yang"))
    print("get返回默认值None:", dict_2.get('name'))
    print("get返回指定值:", dict_2.get('name', "yang"))


def dict_setdefault():
    """方法与get()方法类似，如果键不存在字典中，会添加键并将值设置为默认值"""
    dict_1 = {
        "name": "yanglili",
        "age": 25,
        "sex": 'women',
        "tel": 1893889
    }
    dict_2 = {}
    print("setdefault返回已有值yanglili:", dict_1.setdefault('name'))
    print("setdefault返回已有值yanglili:", dict_1.setdefault('name','yang'))
    print("将name-None加入到字典中", dict_2.setdefault('name'), dict_2)
    print("将name-214加入到字典中", dict_2.setdefault('age','214'), dict_2)


def dict_items():
    """items()返回一个列表视图，列表的元素为键-值对组成的元祖"""
    dict_1 = {
        "name": "yanglili",
        "age": 25,
        "sex": 'women',
        "tel": 1893889
    }
    print('输出字典视图:',dict_1.items())
    print(list(dict_1.items()))

    # 遍历字典视图，获取键和其对应的值
    for i,j in dict_1.items():
        print(i,':',j)

def dict_keys():
    """keys()返回一个由键组成的迭代器
    values()返回一个由值组成的迭代器"""
    dict_1 = {
        "name": "yanglili",
        "age": 25,
        "sex": 'women',
        "tel": 1893889
    }
    print(dict_1.keys())
    print(list(dict_1.keys()))
    print(dict_1.values())
    for i in dict_1.keys():
        print(i)


def dict_update():
    '''dict.update(dict2)将字典2中的key/value(键/值) 对更新到字典 dict中'''
    dict_1 = {
        "name": "yanglili",
        "age": 25,
        "sex": 'women',
        "tel": 1893889
    }
    dict_2 = {'age': 28,'addr': 'shenzhen'}
    dict_1.update(dict_2)
    print(dict_1)


def dict_pop():
    """pop(key[,default])删除指定的键-值，并返回该值,若指定的键不存在，则返回default，如没有指定default，则报错"""
    dict_1 = {
        "name": "yanglili",
        "age": 25,
        "sex": 'women',
        "tel": 1893889,
    }
    print(dict_1.pop('tel'))
    print(dict_1.pop('addr', 'default'))
    print(dict_1)

def dict_popitem():
    """popitem()随机弹出一个字典项"""
    dict_1 = {
        "name": "yanglili",
        "age": 25,
        "sex": 'women',
        "tel": 1893889,
    }
    print(dict_1.popitem())


if __name__ == '__main__':
    dict_clear()
    dict_copy()
    dict_fromkeys()
    dict_get()
    dict_setdefault()
    # dict_items()
    # dict_keys()
    dict_update()
    dict_pop()
    dict_popitem()
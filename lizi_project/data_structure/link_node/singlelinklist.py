# -*- coding: utf-8 -*-
# @Date : 2021/12/19 17:16
# @File : singlelinklist.py
# @Author : Lizi

"""
链表：
    链表是通过一个个节点组成的，每个节点都包含了称为cargo的基本单元，它也是一种递归的数据结构。它能保持数据之间的逻辑顺序，但存储空间不必按照顺序存储。
    链表是一种在存储单元上非连续、非顺序的存储结构。数据元素的逻辑顺序是通过链表中的指针链接次序实现。链表是由一系列的结点组成，结点可以在运行时动态生成。
    每个结点包含两部分：数据域与指针域。数据域存储数据元素，指针域存储下一结点的指针

"""


class Node:
    """
    定义节点：
        节点的数据结构由数据元素（item）和指针（next）组成
        item：存放数据元素
        next：存放指向下一个元素的指针
    """

    def __init__(self, item, next=None):
        self.item = item  # 存放数据元素
        self.next = next  # 存放指向下一个元素的指针


class SingleLinkList:
    """
    定义单向链表：
        链表需要有首地址指针head
    """

    def __init__(self):
        self._head = None

    @property
    def head(self):
        return self._head


# 创建链表
if __name__ == '__main__':
    link_list = SingleLinkList()   # 创建链表
    node1 = Node(1)   # 创建节点1
    node2 = Node(2)   # 创建节点2

    link_list._head = node1   # 将节点加入到链表中
    node1.next = node2   # 将第一个节点的next指向下一节点

    print(link_list.head.item)  # 访问第一个节点数据
    print(link_list.head.next.item)   # 访问第二个节点数据

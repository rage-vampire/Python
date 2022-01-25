# -*- coding: utf-8 -*-
# @Date : 2021/12/19 17:31
# @File : add_two_numbers.py
# @Author : Lizi


class ListNode:
    pass


class Solution:
    def addTwoNumbers(self, l1: ListNode, l2: ListNode) -> ListNode:
        num1 = []
        num2 = []
        while l1:
            num1.append(l1.val)
            l1 = l1.next
        while l2:
            num2.append(l2.val)
            l2 = l2.next
        ret = len(num1) - len(num2)
        if ret < 0:
            ret *= -1
            num1.extend([0] * ret)
        elif ret > 0:
            num2.extend([0] * ret)
        ret = 0
        num3 = []
        for n1, n2 in zip(num1, num2):
            val = (n1 + n2 + ret) % 10
            num3.append(val)
            ret = (n1 + n2 + ret) // 10
        if ret != 0:
            num3.append(ret)
        result = None
        num3.reverse()
        for a in num3:
            result = ListNode(val=a, next=result)
        return result

# -*- coding: utf-8 -*-
# @Date : 2021/7/20 10:16
# @File : 03_isPalindrome.py
# @Author : Lizi


"""给你一个整数 x ，如果 x 是一个回文整数，返回 true ；否则，返回 false 。
回文数是指正序（从左向右）和倒序（从右向左）读都是一样的整数。例如，121 是回文，而 123 不是"""


# 方法一
# def isPalindrome(x: int):
#     if str(x) == str(x)[::-1]:
#         return True
#     else:
#         print(str(x)[::-1])
#         return False


# 方法二：将int转化成str类型: 双指针 (指针的性能一直都挺高的)
# def isPalindrome(x: int) -> bool:
#     lst = list(str(x))
#     L, R = 0, len(lst) - 1
#     while L < R:
#         if lst[L] != lst[R]:
#             return False
#         L += 1
#         R -= 1
#     return True



# 方法三
def isPalindrome(x: int) -> bool:
    if x < 0 or (x % 10 == 0 and x != 0):
        return False
    elif x == 0:
        return True
    else:
        reverse_x = 0
        while x > reverse_x:
            remainder = x % 10   # 取摸运算
            reverse_x = reverse_x * 10 + remainder       # 计算反转后的x的值
            x = x // 10
        # 当x为奇数时, 只要满足 reverse_x//10 == x 即可
        if reverse_x == x or reverse_x // 10 == x:
            return True
        else:
            return False


if __name__ == '__main__':
    rome = isPalindrome(212)
    print(rome)

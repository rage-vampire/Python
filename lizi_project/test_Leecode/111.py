# -*- coding: utf-8 -*-
# @Date : 2021/12/25 13:09
# @File : 111.py
# @Author : Lizi


import math
from typing import List


class Solution:
    def isValid(self, s: str) -> bool:
        if len(s) % 2 == 1:
            return False

        pairs = {
            ")": "(",
            "]": "[",
            "}": "{",
        }
        stack = list()
        for ch in s:
            if ch in pairs:
                if not stack or stack[-1] != pairs[ch]:
                    return False
                stack.pop()
            else:
                stack.append(ch)

        return not stack


if __name__ == '__main__':
    aa = Solution()
    result = aa.isValid('[(}]')
    print(result)

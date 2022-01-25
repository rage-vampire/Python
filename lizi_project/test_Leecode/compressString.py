# -*- coding: utf-8 -*-
# @Date : 2021/12/18 13:35
# @File : compressString.py
# @Author : Lizi


"""
字符串压缩。利用字符重复出现的次数，编写一种方法，实现基本的字符串压缩功能。
比如，字符串aabcccccaaa会变为a2b1c5a3。若“压缩”后的字符串没有变短，则返回原先的字符串。
你可以假设字符串中只包含大小写英文字母（a至z）
"""


class Solution:
    def compressString(self, S: str) -> str:
        if not S:
            return ' '
        ch = S[0]
        cnt = 0
        ans = ''
        for c in S:
            if c == ch:
                cnt += 1
            else:
                ans += ch+str(cnt)
                ch = c
                cnt = 1
        ans += ch+str(cnt)   # 遍历结束后跳转到该步

        return ans if len(ans) < len(S) else S

if __name__ == '__main__':
    com = Solution()
    print(com.compressString('aabbccc'))
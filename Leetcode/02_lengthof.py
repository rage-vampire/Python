# -*- coding: utf-8 -*-
# @Date : 2021/7/19 14:44
# @File : 02_lengthof.py
# @Author : Lizi


def lengthOfLongestSubstring(s: str) -> int:
    string_list = []
    for str in s:

        if str in string_list:
            print(string_list)
            return len(string_list)
        else:
            string_list.append(str)


if __name__ == '__main__':
    s = "ersdf"
    lengthOfStr = lengthOfLongestSubstring(s)
    print(lengthOfStr)

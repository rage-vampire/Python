# -*- coding: utf-8 -*-
# @Date : 2021/7/24 13:57
# @File : 04_romanToInt.py
# @Author : Lizi


def romanToInt(roman_str):
    """罗马数转整数"""
    roman_dict = {
        'I': 1,
        'V': 5,
        'X': 10,
        'L': 50,
        'C': 100,
        'D': 500,
        'M': 1000
    }
    ans = 0
    n = len(roman_str)
    for i, ch in enumerate(roman_str):
        val = roman_dict[ch]
        if i < n - 1 and val < roman_dict[roman_str[i+1]]:
            ans -= val
        else:
            ans += val

    return ans


if __name__ == '__main__':
    print(romanToInt('IV'))

# -*- coding:utf-8 -*-
# @Filename : is_number.py 
# @Author : Lizi
# @Time : 2020/6/22 14:00 
# @Software: PyCharm

def is_number(s):
    try:
        float(s)
        return True
    except ValueError as e:
        # print(e)
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (ValueError,TypeError):
        pass

    return False

print(is_number(23))
print(is_number('fgtre'))
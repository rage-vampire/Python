#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : string_method.py
# @Author: Lizi
# @Date  : 2020/9/9


def str_capitalize():
    """	capitalize()将字符串的第一个字符转换为大写"""

    str = "this is string example from runoob....wow!!!"
    str1 = "@ this is string example from runoob....wow!!!"
    print(str.capitalize())
    print(str1.capitalize())


def str_center():
    """str.center(__width=,__fillchar=)返回一个指定width宽度居中的字符串，fillchar 为填充的字符，默认为空格"""
    str = 'abdgidsfjsaedgbfmktykugjl'
    print(str.center(50))
    print(str.center(50, '-'))


def str_ljust():
    """str.ljust(__width=,__fillchar=),返回一个指定width宽度左对齐的字符串,如果指定的长度小于原字符串的长度则返回原字符串，否则使用fillchar填充值指定长度，
    str.rjust(__width=,__fillchar=) 右对齐"""
    str = 'jsaedgbfmktykugjl'
    print(str.ljust(50))
    print(str.ljust(50, '-'))
    print(str.rjust(50, '-'))


def str_count():
    """count() 方法用于统计字符串里某个字符出现的次数。可选参数为在字符串搜索的开始与结束位置"""

    str = 'abdgidsfjsaedgbfmktykugjl'
    print(str.count('a'))
    print(str.count('a', 0, 5))


def str_decode():
    """bytes.decode(encoding='utf-8',errors='strict')方法，返回解码后的字符串
    str.encode()方法，返回编码后的值，python3中没有decode()方法，我们可以使用bytes对象的decode()方法来解码给定的bytes对象 """
    str = "杨丽丽"
    str_utf = str.encode('UTF-8')
    str_gbk = str.encode("GBK")
    print('utf_编码：', str_utf)
    print('gbk_编码：', str_gbk)
    print('utf_解码:', str_utf.decode('UTF-8'))
    print('gbk_解码:', str_gbk.decode("GBK"))


def str_endswith():
    """str.endswith(obi,strat,end),判断字符串是否以obj结尾，如果是返回True，否则返回false，start和end是可选参数，指定开始和结束位置"""
    str = 'gdjktrindmgi,yll'
    print(str.endswith('yll'))
    print(str.endswith('yll', 0, 10))


def str_find():
    """str.find(obj,start,end),从左边开始查找，在字符串str中查找obj，如果在指定范围包含obj，则返回obj的第一个索引值，否则返回-1，
    str.find(obj,start,end),从右边开始查找，在字符串str中查找obj，如果在指定范围包含obj，则返回obj最后一个索引值，否则返回-1"""
    str = 'python,C++,C,java,golan'
    print(str.find('C'))
    print(str.find('C', 0, 5))
    print(str.rfind('C'))



def str_index():
    """与 find方法一样，只不过如果obj不在str中，会报一个ValueError错误，
    rindex(),从右边开始查找 """
    str = 'python,C++,C,java,golan'
    print(str.index('C'))
    print(str.rindex('l',0,21))


def str_isalnum():
    """检测字符串是否由数字或者字母组成，返回True或者false，
    isalpha()检测字符串是否由字符或者中文组成，
    isdigit()检测字符串是否由数字组成 """
    str = 'yanglili1893889'
    str1 = 'www.python.com'
    print('返回True:', str.isalnum())
    print('返回false:', str1.isalnum())


def str_isnumeric():
    """isnumeric()方法检测字符串是否只由数字组成，数字可以是： Unicode数字，全角数字（双字节），罗马数字，汉字数字。指数类似 ² 与分数类似 ½ 也属于数字"""
    str_a = '123456'
    str_b = '%132143'
    str_c = '\u00B23455'
    print(str_a.isnumeric())
    print(str_b.isnumeric())
    print(str_c.isnumeric())


def str_lower():
    """lower(),返回字符串的小写版本"""
    """islower(),检测字符串的字母是否全部为小写"""
    str = 'ASDFGHJ'
    str_a = 'Yang LI LI'
    str_b = 'fsdjkjg123124**^'
    print('小写字符为', str.lower())
    print('小写字符为', str_a.lower())
    print(str_b.islower())

def str_title():
    """title返回首字母为大写的字符串"""
    """istitle()检测字符串的首字母是否为大写，其他字母为小写，返回True或者false"""
    str = 'yanglili'
    str_a = 'yang li li'
    str_b = 'Yanglili'
    str_c = "Yang Li LI"
    print('返回Yanglili:', str.title())
    print('返回Yang Li Li:', str_a.title())
    print('返回True：', str_b.istitle())
    print('返回fasle：', str_c.istitle())


def str_upper():
    """uppper()返回字符串的大写版本，
    isupper()检测字符串的字符是否全部为大写"""
    str = 'Yang li li'
    str_d = 'SFHJKG'
    print('返回YANG LI LI：', str.upper())
    print('返回True：', str_d.isupper())


def str_strip():
    """strip(__chars) 删除字符串左右两边的指定的字符，参数为空时删除空格，不包括中间的，
    strip(__chars) 删除字符串左边的指定的字符，参数为空时删除空格,
    rstrip(__chars) 删除字符串右边的指定的字符，参数为空时删除空格"""
    str = "  py thon  "
    str_a = "--python--"
    print('返回py thon：',str.strip())
    print('返回python：', str_a.strip('-'))
    print("'返回py thon--':",str_a.lstrip('-'))
    print("'返回--py thon':", str_a.rstrip('-'))


def str_join():
    """join(),用指定的字符串将序列中的元素连接生成一个新的字符串"""
    list1 = ['1', '2', '3', '4', '5']
    tuple1 = ('p', 'y', 't', 'h', 'o', 'n')
    dir = 'C:', 'workspace', 'python'
    sep = '+'
    tu = ''
    str1 = "\\"
    print(sep.join(list1))
    print(tu.join(tuple1))
    print(str1.join(dir))


def str_split():
    """str.split(str="", num=string.count(str)),用指定的字符将序列拆分，返回拆分后的列表
    如果第二个参数 num 有指定值，则分割为 num+1 个子字符串"""
    str = "1=2=3=4=5"
    print(str.split('='))     # 返回 ['1', '2', '3', '4', '5']
    print(str.split('=', 2))  # 返回 ['1', '2', '3=4=5']

    url = "http://www.baidu.com/python/image/123456.jpg"
    print(url.split('/')[-1])   # 爬虫时可以用此方法获取图片名称


def str_replace():
    """str.replace(old,new),用new替换字符串中指定的字符"""
    str = 'www.taobao.com'
    print(str.replace('taobao','baidu'))


def str_maketrans():
    """str.maketrans(intab, outtab)用于创建字符映射的转换表，对于接受两个参数的最简单的调用方式，
    第一个参数是字符串，表示需要转换的字符，第二个参数也是字符串表示转换的目标。两个字符串的长度必须相同，为一一对应的关系
    bytearray.maketrans()、bytes.maketrans()、str.maketrans()"""
    intab = 'abcde'
    outtab = '12345'
    make_table = str.maketrans(intab,outtab)
    print(type(make_table))
    print(make_table)    # 返回转换字符的Unicode码点之间的转换关系，类型为dict
    str_a = 'abcdefghijk'
    print(str_a.translate(make_table))

def str_translate():
    """str.translate(table)方法根据参数table给出的表(包含 256 个字符)转换字符串的字符,要过滤掉的字符放到 deletechars 参数中。
    str.translate(table)
    bytes.translate(table[, delete])
    bytearray.translate(table[, delete]"""

    str_maketable = bytes.maketrans(b'abcdefghijklmnopqrstuvwxyz',b'ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    str_a = b'python'
    print(str_a.translate(str_maketable, b'o'))


def str_swapcase():
    """swapcase() 方法用于对字符串的大小写字母进行转换"""
    str = 'yang LILI'
    print(str.swapcase())


def str_test():
    '''间隔输出大小写字母'''
    new_str = []
    str_a = 'djsignsdgjkrymh'
    for index, ele in enumerate(str_a):
        if index % 2 == 0:
            ele = ele.title()
            new_str.append(ele)
            # print(new_ele)
        else:
        # if index % 2 != 0:
            ele = ele.lower()
            new_str.append(ele)
    print(new_str)


def san():
    width = 5
    l1 = ' '
    n = int(input('请输入n：'))
    for i in range(1, n+1):
        t = i * ' * '
        t1=t.center(len(t))
        # print(t1)
        print(t1.center((n * width), '-'))




if __name__ == '__main__':
    # str_capitalize()
    str_center()
    # str_ljust()
    # str_count()
    # str_decode()
    # str_endswith()
    # str_find()
    # str_index()
    # str_isalnum()
    # str_isnumeric()
    # str_lower()
    # str_title()
    # str_upper()
    # str_strip()
    # str_join()
    # str_split()
    # str_replace()
    # str_swapcase()
    # str_maketrans()
    # str_translate()
    # str_test()
    san()
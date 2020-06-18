# -*- coding:utf-8 -*-
# @Filename : defaultdict.py 
# @Author : Lizi
# @Time : 2020/6/17 10:44 
# @Software: PyCharm


from collections import defaultdict

strings = ('puppy', 'kitten', 'puppy', 'puppy','weasel', 'puppy', 'kitten', 'puppy')
counts = defaultdict(int)
for kw in strings:
    counts[kw] += 1
print(counts)


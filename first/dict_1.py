# -*- coding: utf-8 -*-
# @file   : dict_1.py
# @author : lizi
# @date   : 2019/9/23
# @version: 1.0
# @desc   :

people = {
    "Alice":{
        'phone':123456,
        'addr':'Foo drive 23'
    },
    "Beth":{
        'phone':8899,
        'addr':'Bar street 42'
    },
    "Cecil":{
        'phone':3158,
        'addr':'Baz avenue 90'
    }
}
labels = {
    'phone':'phone number',
    'addr':'address'
}
name = input('Name:')
request = input('Phone number (p) or address (a)?' )
if request == 'p':
    key = 'phone'
elif request == 'a':
    key = 'addr'
else:
    print("111")
if name in people:
    if key in labels[key]:
        print("{}`s {} is {}".format(name,labels[key],people[name][key]))
else:
    print("name does not exist ,Please re-enter!")
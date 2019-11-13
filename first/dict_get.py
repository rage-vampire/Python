# -*- coding: utf-8 -*-
# @file   : dict_get.py
# @author : lizi
# @date   : 2019/9/24
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
request = input('Phone number (p) or address (a)?')
key = None
if request == 'p':key = 'phone'
if request == 'a':key = 'addr'
person = people.get(name,{})
label = labels.get(name,key)
result = person.get(key,'not available')
print("{}`s {} is {}.".format(name,label,result))


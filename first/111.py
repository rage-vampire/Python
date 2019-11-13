# -*- coding: utf-8 -*-
# @file   : 111.py
# @author : lizi
# @date   : 2019/9/24
# @version: 1.0
# @desc   :

labels = {
    'phone':'phone number',
    'addr':'address'
}
#返回字典键值的对数，即计算字典的长度
print(len(labels))
#获取phone的值
print(labels['phone'])
#删除键addr
del labels['addr']
#修改键phone的值
labels['phone']="phone number is 8899"
print(labels)
#检查键是否在字典中
print('phone' in labels)
print ('addr' in labels)
#给字典添加键值
labels['name'] = 'firstname'
print(labels)
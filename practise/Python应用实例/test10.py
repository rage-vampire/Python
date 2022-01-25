# 五、请写下列代码的运行结果
import copy
#赋值、浅拷贝、深拷贝的区别
alist=[1,2,3,["a","b"]]
#直接赋值,传递对象的引用而已,原始列表改变，被赋值的b也会做相同的改变
b = alist
print(b)
#结果：[1, 2, 3, ['a', 'b']]
alist.append(5)
print(alist)
#结果：[1, 2, 3, ['a', 'b'], 5]
print(b)
#结果：[1, 2, 3, ['a', 'b'], 5] #alist列表里的值变了，列表里也会改变 。

#2、copy浅拷贝，没有拷贝子对象，所以原始数据改变，子对象会改变
b = copy.copy(alist)
print(b)
#结果：[1, 2, 3, ['a', 'b']]
alist.append(5)
print(alist)
#结果：[1, 2, 3, ['a', 'b'], 5]
print(b)
#结果：[1, 2, 3, ['a', 'b']] #b列表对象的值没有变。
alist[3].append('cccc') #给alist的子列表对象增加了值
print(b)
#结果：[1, 2, 3, ['a', 'b',"cccc"]] #b中的子列表对象也同步发生了修改。
print(alist)
[1, 2, 3, ['a', 'b',"cccc"], 5]

#3、deepcopy深拷贝，包含对象里面的自对象的拷贝，所以原始对象的改变不会造成深拷贝里任何子元素的改变
b = copy.deepcopy(alist)
print(b)
#结果：[1, 2, 3, ['a', 'b']]
alist.append(5)
print(alist)
#结果：[1, 2, 3, ['a', 'b'], 5]
print(b)
#结果：[1, 2, 3, ['a', 'b']] #随便alist怎么修改，b都不会变。
alist[3].append('cccc') #给alist的子列表对象增加了值
print(alist)
#结果：[1, 2, 3, ['a', 'b',"cccc"], 5]
print(b)
#结果：[1, 2, 3, ['a', 'b']] #随便alist怎么修改，b都不会变。

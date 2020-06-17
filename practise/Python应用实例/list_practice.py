# -*- coding:utf-8 -*-
# @Filename : list_practice.py 
# @Author : Lizi
# @Time : 2020/3/10 9:22 
# @Software: PyCharm

names=['Lihua','Rain','jack','xiuxiu','peiqi','Black']
# 往names列表里Black前面插入一个Blue。
names.insert(-1,'Blue')
# 把names列表中Xiuxiu的名字改成中文
names[3]="秀秀"                         # 或 names[names.index("xiuxiu")]="秀秀"
# 往names列表中Rain后面插入一个子列表["oldboy","oldgirl"]。
names[2:2]=["odlboy",'odlgirl']
# 返回names列表中Peiqi的索引值
print(names.index("peiqi"))
# 创建新列表[1,2,3,4,2,5,6,2,]，合并到names列表中。
num = [1,2,3,4,2,5,6,2,]
names.extend(num)
# 取出names列表中索引4-7的元素。
print(names[4:8])
# 取出names列表中索引2-10的元素，步长为2。
print(names[2:11:2])
# 取出names列表中最后3个元素。
print(names[-3:])
# 循环names列表，打印每个元素的索引值和元素。
for item in names:
    print(item,names.index(item))
# 11、循环names列表，打印每个元素的索引值和元素，当索引值为偶数时，把对应的元素改成-1。
# for index,item in enumerate(names):
#     if index % 2 == 0:
#         names[index] = -1

# **************************************************************************************
# 12、names列表里有3个2，请返回第二个2的索引值，不要人肉，要动态找
count = 0
for index,item in enumerate(names):
    if item == 2:
        count += 1
        while count == 2:
            print("第二个2的索引值为：" + str(index))
            break
    else:
        continue
print(names)

# *****************************************************************************************
'''13、现有商品列表如下：
products = [["iphone",6888],["MacPro",14800],["小米6",2499],
            ["Coffee",31],["Book",60],["Nike",699]]，需打印出以下格式：
------  商品列表 ------
 iphone    6888
 MacPro    14800
 小米6        2499
 Coffee      31
 Book        60
 Nike         69 '''
# products = [["iphone",6888],["MacPro",14800],["小米6",2499],["Coffee",31],["Book",60],["Nike",699]]
# print("------商品列表------")
# for index,item in enumerate(products):
#     print(item[0] + '  ',item[1])

# 14、根据products列表写一个循环，不断询问用户想买什么，用户选择一个商品编号，就把对应的商品添加到购物车里，最终用户输入q退出时，打印购买的商品列表。
shop_car = []
shop_cost = 0
products = [["iphone",6888],["MacPro",14800],["小米6",2499],["Coffee",31],["Book",60],["Nike",699]]
exit_log = True
while exit_log:
    print("------ 商品列表 ------")
    for index, i in enumerate(products):
        print(index, i[0], i[1])
    user_choice = input("\n输入你想购买的产品序号(按“q”退出):")
    # if user_choice.isdigit():                                                             # 判断用户输入的是否是数字
    user_choice = int(user_choice)                                                    # 强制转换为数字
    if user_choice >= 0 and user_choice < len(products):                              # 判断用户购买的商品是否在商品列表中
        shop_car.append(products[user_choice])                                        # 加入购物车
        shop_cost += products[user_choice][1]                                         # 计算费用
        # print(shop_cost)
        print("\n %s 已经加入你的购物车\n" % products[user_choice])
    else:
        print("抱歉，此商品不存在\n")

    if user_choice == "q":                                                            # 用户选择退出
        if len(shop_car) > 0:                                                         # 判断用户是否购买了商品
            print("\n------ 你的购物车 ------")
            for index, i in enumerate(shop_car):                                      # index和i为临时变量，与前一个for循环里index和i作用的列表不同，故可重用
                print("%s  %s" % (i[0], i[1]))
            print("\n你此次购物的花费合计是:%s元\n" % shop_cost)
            exit_log = True  # 退出购物
        else:
            exit_log = True  # 未购买商品，不打印购物车商品，直接退出
    else:
        # 输入不合法
        exit_log = True






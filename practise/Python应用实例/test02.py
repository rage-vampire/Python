#冒泡排序 复杂度O(n^2)
list = [9, 1, 4, 6, 2, 10, 15, 12, 8, 11,17]

list.insert(0,list.pop(1))
print(list)

def bubbling(list_init):
    for i in range(len(list_init)-1):
        for j in range(len(list_init)-1-i):
            if list_init[j] > list_init[j+1]:
                t = list_init[j]
                list_init[j] = list_init[j+1]
                list_init[j+1] = t
print(list)
bubbling(list)

#插入排序 复杂度O(n^2)
def insert_sort(list_init):
    for i in range(1,len(list_init)):
        for j in range(i):
            if list_init[i] < list_init[j]:
                #list_init.insert(j,list_init.pop(i))
                list_init[i],list_init[j] = list_init[j],list_init[i]
    return list_init

list2 = [9, 1, 4, 6, 2, 10, 15, 12, 8, 11,17]
print(insert_sort(list2))

#
#快速排序 复杂度O(log2n)
# data = [45, 3, 2, 6, 3, 78, 5, 44, 22, 65, 46]
#
# def quickSort(data, start, end):
#     i = start
#     j = end
#     # i与j重合时，一次排序结束
#     if i >= j:
#         return data
#     # 设置最左边的数为基准值
#     flag = data[start]
#     while i < j:
#         while i < j and data[j] >= flag:
#             j -= 1
#         # 找到右边第一个小于基准的数，赋值给左边i。此时左边i被记录在flag中
#         data[i] = data[j]
#         while i < j and data[i] <= flag:
#             i += 1
#         # 找到左边第一个大于基准的数，赋值给右边的j。右边的j的值和上面左边的i的值相同
#         data[j] = data[i]
#     # 由于循环以i结尾，循环完毕后把flag值放到i所在位置。
#     data[i] = flag
#     # 除去i之外两段递归
#     quickSort(data, start, i - 1)
#     quickSort(data, i + 1, end)
#
# quickSort(data,0, len(data)-1)
# print(data)

#
# def quickSort(datalist):
#     if datalist == []:
#         return datalist
#     else:
#         first = datalist[0]
#         less = quickSort([i for i in datalist[1:] if i < first])
#         more = quickSort([j for j in datalist[1:] if j >= first])
#         return less+[first]+more
# sortlist = quickSort(data)
# print(sortlist)





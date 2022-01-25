#二分查找,给出一个已经排好序的列表,注意是已经排好序的,查找指定元素在列表中的位置
def binary_search(order_list, item):
    low = 0
    high = len(order_list) - 1
    while high - low > 1:
        middle = (low + high) // 2
        if order_list[middle] < item:
            low = middle + 1
        elif order_list[middle] > item:
            high = middle - 1
        else:
            return middle
    if high - low == 1:
        if order_list[low] == item:
            return low
        if order_list[high] == item:
            return high
    if high - low == 0:
        return high


order_list = [2, 3, 4, 6, 89, 99]
item = 2
print(binary_search(order_list, item))

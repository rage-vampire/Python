#有一组“+”和“-”符号，要求将“+”排到左边，“-”排到右边，写出具体的实现方法

def StringSort(data):
    startindex = 0
    endindex = 0
    count = len(data)
    while startindex + endindex < count:
        if data[startindex] == '-':
            data[startindex], data[count - endindex - 1] = data[count - endindex - 1], data[startindex]
            endindex += 1
            print('1')

        else:
            startindex += 1
            print('2')
    return data

data = ['-', '-', '+', '+', '+','-', '+','-', '+','-','-']
print(StringSort(data))
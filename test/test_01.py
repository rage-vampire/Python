def outer_func(f):
    b = 10

    def inner(x: int, y: int):
        return b + f(x, y)

    return inner


# @outer_func    sum = outer_func(sum)
def sum(x, y):
    print('qwertyuiop')
    return x + y


if __name__ == '__main__':
    fo = outer_func(sum)
    print(fo(2, 3))
    # print(sum(2,3))
    # print(fo(2, 3))
    # val = sum(2, 3)
    # print(val)

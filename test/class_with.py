import datetime


class context_simple_demo:
    def __init__(self):
        """构造函数，在创建类对象的时候被调用"""
        print('------Create on object-------')
        self._birthday = datetime.datetime.now()

    def __enter__(self):
        """申请资源，这里只打印函数的调用信息"""
        print('Invoke __enter__')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """释放资源，这里只打印函数的调用信息"""
        print('Invoke __exit__')
        if exc_type:
            print('exc_type:{}'.format(exc_type))
            print('exc_val:{}'.format(exc_val))
            print('exc_tb:{}'.format(exc_tb))

    @property        # property装饰器，将birthday函数当做属性访问
    def birthday(self):
        return self._birthday


if __name__ == '__main__':
    with context_simple_demo() as f:
        print(f.birthday)
        # raise Exception("raise an exception")

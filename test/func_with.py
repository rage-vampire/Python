import sys
from contextlib import contextmanager


@contextmanager
def context_demo(para: str):
    """使用 contextmanager 装饰器让这个函数支持上下文管理"""
    f = None
    try:
        print("******enter context_demo:{}".format(para))
        f = open(sys.argv[0], mode='r', encoding='utf-8')
        yield f

    finally:
        print("______exit context_demo:{}".format(para))
        if f is not None:
            f.close()


if __name__ == '__main__':
    with context_demo("test") as f:
        # print(type(f))
        for line in f:
            print(line, end=' ')


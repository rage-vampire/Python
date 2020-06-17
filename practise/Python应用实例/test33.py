#安全线程单例模式
import threading

def synchronized(func):
    func.__lock__ = threading.Lock()

    def lock_func(*args, **kwargs):
        with func.__lock__:
            return func(*args, **kwargs)

    return lock_func

class Singleton(object):
    instance = None

    @synchronized
    def __new__(cls, *args, **kwargs):
        """
        :type kwargs: object
        """
        if cls.instance is None:
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self, num):
        self.a = num + 5

    def printf(self):
        print(self.a)


a = Singleton(3)
print(id(a))
b = Singleton(4)
print(id(b))


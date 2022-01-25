class Person(object):
    '''声明一个 Person 类，有名字、性别和年龄三个属性'''

    def __init__(self, name: str, sex: str, age: int):
        self._name = name
        self._sex = sex
        self._age = age

    @property
    def name(self):
        '''name 属性，读取 self._name'''
        return self._name

    @name.setter
    def name(self, new_name):
        '''name 属性设置器'''
        self._name = new_name

    @property
    def sex(self):
        '''sex 属性，读取 sefl._sex'''
        return self._sex

    @property
    def age(self):
        '''age 属性，读取 self._age'''
        return self._age

    @age.setter
    def age(self, new_age):
        '''age 属性设置器'''
        self._age = new_age


if __name__ == '__main__':
    one = Person(name="xiaoming", sex="M", age=25)
    print("Init info: name={}, sex={}, age={}.".format(one.name, one.sex, one.age))
    one.name = "daming"
    # one.sex="F" 没有办法设置 sex 的值，因为 sex 是只读属性（因为没有实现 sex.setter）
    one.age = "26"
    print("Show info: name={}, sex={}, age={}.".format(one.name, one.sex, one.age))
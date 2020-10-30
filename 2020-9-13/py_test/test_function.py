# -*- coding:utf-8 -*-
# @Filename : test_function.py 
# @Author : Lizi
# @Time : 2020/4/14 9:23 
# @Software: PyCharm
import pytest
import function_demo


@pytest.mark.usefixtures(scope='class')
def start():
    print("---------------------开始测试--------------------")
    print('----------------------done----------------------')


class Test_function_demo:
    # def setup_method(self):
    #     print("---------------------开始测试--------------------")
    #
    # def teardown(self):
    #     print('----------------------done----------------------')

    def test_add_int(self):
        try:
            assert (function_demo.add(2, 3) == 5)
        except AssertionError as e:
            raise e
            print(e)

    def test_sub_int(self):
        try:
            assert (function_demo.sub(6, 2) == 4)
        except AssertionError as e:
            raise e
            print(e)

    def test_sub_float(self):
        try:
            assert (function_demo.sub(10.79, 5.01) == 5.78)
        except AssertionError as e:
            raise e
            print(e)

    def test_f(self):
        with pytest.raises(SystemError):
            function_demo.f()

    def test_tmpdie(self,tmpdir):
        print(tmpdir)
        assert 0


if __name__ == '__main__':
    pytest.main(['-s', 'test_function.py'])

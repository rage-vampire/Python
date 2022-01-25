# -*- coding:utf-8 -*-
# @Filename : test_xfail.py
# @Author : Lizi
# @Time : 2020/4/17 8:54 
# @Software: PyCharm


import pytest
# 预期失败

class TestCase():
    @pytest.mark.xfail(condition=1 < 2, reason="预期失败，执行失败")
    def test_case01(self):
        '''01预期失败，执行也是失败'''
        print('执行用例01......')
        assert 0

    @pytest.mark.xfail(condition=1 < 2, reason="预期失败，执行成功")
    def test_case02(self):
        """02预期失败，但实际结果却执行成功了"""
        print("执行用例02........")
        assert 1

    @pytest.mark.xfail(condition=1 > 2, reason="预期成功，执行成功")
    def test_case03(self):
        """03预期成功，实际执行结果也是成功"""
        print("执行用例03........")
        assert 1

    @pytest.mark.xfail(condition=1 > 2, reason="预期成功，执行失败")
    def test_case04(self):
        """04预期成功，实际执行结果失败了"""
        print("执行用例04........")
        assert 0

    def test_case05(self):
        print("执行成功的用例05........")
        assert 1

    def test_case06(self):
        print("执行失败的用例06........")
        assert 0


# 参数化：将要测试的参数分别传递给测试函数

mobile_list = ['10010', '10086']
code_list = ['x2xx', '45gr']

# """手机号和验证码分别组合，产生四组测试用例"""
# @pytest.mark.parametrize('mobile', mobile_list)
# @pytest.mark.parametrize('code', code_list)

"""手机号与验证码一一对应组合，使用zip函数，并行迭代"""
@pytest.mark.parametrize('mobile,code',zip(mobile_list,code_list))
def test_register(mobile, code):
    """通过手机号注册"""

    print("注册手机号是:{},验证码是：{}".format(mobile, code))


if __name__ == '__main__':
    pytest.main(['-s', 'test_xfail.py'])

# -*- coding:utf-8 -*-
# @Filename : test42.py 
# @Author : Lizi
# @Time : 2020/3/24 21:59 
# @Software: PyCharm

#
# def faulty():
#     raise Exception("somthing is wrong")
#
#
# def ignore_exception():
#     faulty()
#
#
# def handle_exception():
#     try:
#         faulty()
#     except:
#         print("Exception handle")

# faulty()


from warnings import warn
from warnings import filterwarnings
# filterwarnings("error")
# warn("dkgfmnbk",DeprecationWarning)
warn("......")
filterwarnings("ignore")
warn("////////")

# 自定义异常
# class CustomError(Exception):
#     def __init__(self, ErrorInfo):
#         # super(self).__init__(self)
#         self.error = ErrorInfo
#
#     def aa(self):
#         return self.error
#
# if __name__ == '__main__':
#     try:
#         raise CustomError()
#     except CustomError as e:
#         # except Exception as e:
#         print(e)

# 自定义异常
# class Name(Exception):
#     pass
# try:
#     raise Name("wtju")
# except Name as e:
#     print(e)
#     print("dshag")
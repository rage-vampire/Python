#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : students.py
# @Author: Lizi
# @Date  : 2020/10/21


# def sno_sort_01(li):
#     new_list = sorted(li, key=lambda dic: dic['sno'])
#     for i in new_list:
#         if i['sex'] == 'male':
#             print('男生的信息如下:{}'.format(i))
#
#
# def sno_sort_02(li):
#     li.sort(key=lambda dic: dic['sno'])
#     for i in li:
#         if i['classmate'] == '101':
#             print('101班级的学生信息如下:')
#             print(i)
#
#
# def score_sort(li):
#     new_list = sorted(li, key=lambda dic: (dic['score'], dic['sno']))
#     print(new_list)
#
#
# if __name__ == '__main__':
#     infos_list = []
#     for i in range(3):
#         infos = {}
#         infos['name'] = input('请输入姓名：')
#         infos['sno'] = int(input('请输入学号：'))
#         infos['sex'] = input('请输入性别:')
#         infos['classmate'] = input('请输入班级:')
#         infos['score'] = int(input('请输入分数:'))
#         infos_list.append(infos)
#     # sno_sort_01(infos_list)
#     # sno_sort_02(infos_list)
#     score_sort(infos_list)


class Student():

    def sno_sort_01(self, info_list):
        new_list = sorted(info_list, key=lambda dic: dic['sno'])
        for i in new_list:
            if i['sex'] == 'male':
                print('男生的信息如下:{}'.format(i))
                print(i)

    def sno_sort_02(self, info_list):
        info_list.sort(key=lambda dic: dic['sno'])
        for i in info_list:
            if i['classmate'] == '101':
                print('101班级的学生信息如下:{}'.format(i))


    def score_sort(self,info_list):
        new_list = sorted(info_list, key=lambda dic: (dic['score'], dic['sno']))
        print(new_list)


if __name__ == '__main__':
    infos_list = []
    for i in range(3):
    # while True:
        infos = {}
        infos['name'] = input('请输入姓名：')
        infos['sno'] = int(input('请输入学号：'))
        infos['sex'] = input('请输入性别:')
        infos['classmate'] = input('请输入班级:')
        infos['score'] = int(input('请输入分数:'))
        infos_list.append(infos)

    stu = Student()
    stu.sno_sort_02(infos_list)
    # sno_sort_01(infos_list)
    # sno_sort_02(infos_list)
    # score_sort(infos_list)
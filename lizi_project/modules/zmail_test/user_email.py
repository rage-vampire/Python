#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : user_email.py
# @Author: Lizi
# @Date  : 2020/11/18

from zmail_test import Email
import zmail_test
import xlrd
import openpyxl

'''
    Python群发一个excel表格中的所有联系人的邮件
        1.多个sheet表格依次发送所有的邮件
        2.每个邮件的内容不一样
'''
def user():
    excel1 = openpyxl.load_workbook('email.xlsx')
    all_sheet = excel1.worksheets
    receiver_user =[]
    for sheet in all_sheet:
        for cell in list(sheet.columns)[0]:
            receiver_user.append(cell.value)

    return receiver_user


def email_msg():
    excel1 = openpyxl.load_workbook('email.xlsx')
    all_sheet = excel1.worksheets
    msg_list = []
    for sheet in all_sheet:
        for cell in list(sheet.columns)[1]:
            msg_list.append(cell.value)

    return msg_list


if __name__ == '__main__':
    receiver_user_list = user()
    email_msg_list = email_msg()
    sub = '群发邮件主题'
    attach = ('email.xlsx', 'email.html')
    sender = ('rage_vampire0626@163.com', 'KNRNPQDNBHRLQUAP')
    # with open('email.txt', 'r', encoding='utf-8') as f:
    #     con = f.read()
    for i in range(len(receiver_user_list)):
        email = Email(sub, email_msg_list[i], *attach)
        email.send_msg(sender, receiver_user_list[i])




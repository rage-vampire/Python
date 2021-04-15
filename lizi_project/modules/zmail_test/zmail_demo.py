#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : zmail_demo.py
# @Author: Lizi
# @Date  : 2020/11/18

import zmail

'''
    1、发送的邮件内容
        1、subject：邮件主题
        2、content_text：文本邮件
        3、content_html：html邮件
        4、attachements：附件
'''


# 发件人邮箱账号和授权码
sender = ('rage_vampire0626@163.com', 'KNRNPQDNBHRLQUAP')

# 收件人邮箱账号
reveiver =['rage_vampire0626@163.com', '1292451946@qq.com']

# 发送的消息体
msg = {
    'subject': '测试邮件',
    'content_text': 'iujkdshfiwenkldsghietb',
    'attachements': 'email.xlsx'
}


# 发件人登陆邮箱账号
server = zmail.server(sender[0], sender[1])

# 发送消息
server.send_mail(reveiver, msg)
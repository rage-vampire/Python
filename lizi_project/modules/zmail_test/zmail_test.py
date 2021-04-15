#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : zmail_test.py
# @Author: Lizi
# @Date  : 2020/11/17

import zmail


class Email:
    """
        邮件内容：主题subject、文本正文content_text、邮件正文content_html、附件attachments
        多个附件放在列表中，用逗号隔开
        发件人
        收件人：多个收件人放在列表中，用逗号隔开
        发件人登陆邮箱
        发送邮件
    """

    def __init__(self, subject, content, *attachments):
        self.subject = subject
        self.content = content
        self.attachments = attachments
        self.msg = {
            'subject': self.subject,
            'content_text': self.content,
            'attachments': list(self.attachments)
        }

    def send_msg(self, sender, *receiver):
        self.sender = sender
        # self.receiver = []
        self.receiver = receiver
        #
        # # 发件人登陆
        self.server = zmail.server(*self.sender)
        # for i in receiver.values():
        #     self.receiver.append(i)
        #     self.server.send_mail(self.receiver, self.msg)

        self.server.send_mail(*self.receiver, self.msg)


if __name__ == '__main__':
    sub = '发送邮件主题'
    attach = ('email.xlsx', 'email.html')
    with open('email.txt', 'r', encoding='utf-8') as f:
        con = f.read()

    sender = ('rage_vampire0626@163.com', 'KNRNPQDNBHRLQUAP')
    receiver = ['rage_vampire0626@163.com', '1292451946@qq.com']

    email = Email(sub, con, *attach)
    email.send_msg(sender, receiver)

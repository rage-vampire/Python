# -*- coding: utf-8 -*-
# !/usr/bin/python
# @Author: WX
# @Create Time: 2020/5/26
# @Software: PyCharm

from testcase.ws_testcase.tool.simple_app import SimpleAppFunc
import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='App for market subscribing')
    parser.add_argument(
        '--addressIp',
        '-a',
        help=u'subscribing address ip, default ip is 192.168.80.211',
        default='192.168.80.211')
    parser.add_argument(
        '--port',
        '-p',
        help=u'subscribing address port, default port is 12511',
        default='12511')
    args = parser.parse_args()
    address = args.addressIp
    port = args.port
    url = 'ws://' + address + ':' + port
    app = SimpleAppFunc(url)
    app.listen_and_action()
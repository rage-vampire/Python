#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : 04_interface_related.py
# @Author: Lizi
# @Date  : 2020/12/15

import requests
import json

"""
    接口关联：一个接口的返回值为另一接口的入参
"""

"""
    实例一：将新建主题返回的主题id传给修改主题接口
"""


class Topic:

    """关于主题的操作：新建、修改、收藏、取消等"""

    def __init__(self):
        self.URL = "http://49.233.108.117:3000/api/v1"

    def add_topic(self):
        """
            新建topic，通过返回的message信息获取返回的'topic_id'
        """
        add_topic_data = {
            "title": '这是新增的topic',
            "tab": "share",
            "content": "通过python脚本发送的主题",
            "accesstoken": "a9c664c5-9ad8-4f1f-9197-e46687374386"
        }
        content_type = {"Content-Type": "application/json"}
        self.res_topic = requests.post(url=self.URL + "/topics", json=add_topic_data, headers=content_type)
        # print(json.dumps(self.res_topic.json(), indent=4, ensure_ascii=False))
        # print(self.res_topic.json()['topic_id'])
        return self.res_topic.json()

    def update_topic(self):
        """
            修改topic，通过新建topic返回的'topic_id'，修改该topic的信息
        """
        update_topic_data = {
            "title": '这是修改的topic',
            "topic_id": self.add_topic()['topic_id'],   # 获取 topic_id
            "tab": "share",
            "content": "通过python脚本发送的主题",
            "accesstoken": "a9c664c5-9ad8-4f1f-9197-e46687374386"
        }
        content_type = {"Content-Type": "application/json"}
        update_res_topic = requests.post(url=self.URL + "/topics/update", json=update_topic_data,
                                         headers=content_type)
        return update_res_topic.json()


if __name__ == '__main__':
    topic = Topic()
    update = topic.update_topic()
    print(json.dumps(update, indent=4))
    assert update["success"] == True

# def add_topic():
#     URL = "http://49.233.108.117:3000/api/v1"
#
#     add_topic_data = {
#         "title": '这是新增的topic',
#         "tab": "share",
#         "content": "通过python脚本发送的主题",
#         "accesstoken": "a9c664c5-9ad8-4f1f-9197-e46687374386"
#     }
#     content_type = {"Content-Type": "application/json"}
#     res_topic = requests.post(url=URL+"/topics", json=add_topic_data, headers=content_type)
#     print(json.dumps(res_topic.json(), indent=4, ensure_ascii=False))
#     print(res_topic.json()['topic_id'])
#     return res_topic.json()
#
#
# def update_topic():
#     URL = "http://49.233.108.117:3000/api/v1"
#     update_topic_data = {
#         "title": '这是修改的topic',
#         "topic_id": add_topic()['topic_id'],
#         "tab": "share",
#         "content": "通过python脚本发送的主题",
#         "accesstoken": "a9c664c5-9ad8-4f1f-9197-e46687374386"
#     }
#     content_type = {"Content-Type": "application/json"}
#     update_res_topic = requests.post(url=URL + "/topics/update", json=update_topic_data, headers=content_type)
#
#     return update_res_topic.json()
#
# update = update_topic()
# print(update)

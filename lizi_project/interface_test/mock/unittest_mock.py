#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : unittest_mock.py
# @Author: Lizi
# @Date  : 2020/12/21

import unittest
from unittest import mock
import requests


class Mock(unittest.TestCase):
    def setUp(self) -> None:
        self.url = "http://127.0.0.1/api/order/create/cc3bdda5c61ad0900474b6e095704105"

    def tearDown(self) -> None:
        pass

    def test_case_01(self):
        data = {
            "real_name": "",
            "phone": "",
            "addressId": 1,
            "useIntegral": 0,
            "couponId": 0,
            "payType": "yue",
            "pinkId": 0,
            "seckill_id": 0,
            "combinationId": 0,
            "bargainId": 0,
            "from": "weixinh5",
            "mark": "",
            "shipping_type": 1,
            "store_id": 0
        }
        # 创建mock响应数据对象
        mock_res = requests.Response()
        # 设置状态码
        mock_res.status_code = 200
        # 设置返回的body数据
        mock_res._content = {"status": 200, "msg": "微信支付成功",
                             "data": {"status": "SUCCESS",
                                      "result": {"orderId": "wx160846682663298919",
                                                 "key": "cc3bdda5c61ad0900474b6e095704105"}}}
        with mock.patch.object(requests, 'post', return_value=mock_res):
            res = requests.post(self.url, data)
            # 设置的返回的body是json格式的，因此不能使用res.text获取body数据，只能使用res.content获取body数据
            print(res.content)
        return res.content


if __name__ == '__main__':
    unittest.main()

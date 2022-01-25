# -*- coding: utf-8 -*-
# !/usr/bin/python
# @Author: WX
# @Create Time: 2020/6/16
# @Software: PyCharm

import rocksdb
from common.test_log.ed_log import get_log


class RocksDBClient(object):
    def __init__(self, db_path):
        self.db = rocksdb.DB(db_path, rocksdb.Options(create_if_missing=False), read_only=True)
        self.logger = get_log()

    def get(self, key):
        key = bytes(key, encoding='utf-8')
        return self.db.get(key)


if __name__ == '__main__':
    rocksdb_path = '/mnt/test_rocksdb'
    db = RocksDBClient(rocksdb_path)
    print(db.get('KLINE_16_HHI2006_10_20200615160000'))
    print(db.get('testkey1'))
    print(db.get('testkey2'))
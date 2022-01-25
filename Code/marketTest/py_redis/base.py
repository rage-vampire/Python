# -*- coding: utf-8 -*-
# !/usr/bin/python
# @Author: WX
# @Create Time: 2020/6/20
# @Software: PyCharm

import redis
from test_config import *
from common.test_log.ed_log import get_log
from common.common_method import Common


class RedisDb(object):
    def __new__(cls, *args, **kwargs):
        # 单例模式
        if not hasattr(cls, 'instance'):
            cls.instance = super(RedisDb, cls).__new__(cls)
        return cls.instance

    def __init__(self, host=redis_host, port=redis_port):
        self.host = host
        self.port = port
        self.conn = self.__connectPika(self.host, self.port)
        self.logger = get_log()
        self.common = Common()

    def loadPikaConfig(self, host, port):
        self.host = host
        self.port = port

    def __connectPika(self, host, port):
        pool = redis.ConnectionPool(host=host, port=port, db=0)
        r = redis.Redis(connection_pool=pool)
        return r

    def __dictget(self, dict1, obj, default=None):
        for k, v in dict1.items():
            if k == obj:
                return v
            else:
                if type(v) is dict:
                    re = self.__dictget(v, obj)
                    if re is not default:
                        return re

    def GetHashKeyVaule(self, key):
        re = self.conn
        if re.exists(key):
            return re.hgetall(key)
        else:
            msg = 'no key'
            return msg

    def GetHashFieldVaule(self, key, field):
        re = self.conn
        if re.exists(key):
            return self.dictInDictGetValue(re.hgetall(key), field)
        else:
            msg = 'no key'
            return msg

    def GetSetVaule(self, key):
        re = self.conn
        if re.exists(key):
            return re.smembers(key)
        else:
            msg = 'no key'
            return msg

    def GetStrValue(self, key):
        re = self.conn
        if re.exists(key):
            return re.get(key)
        else:
            msg = 'no key'
            return msg

    def GetListValues(self, key):
        re = self.conn
        if re.exists(key):
            return re.lrange(key, 0, -1)
        else:
            msg = 'no key'
            return msg

    def GetListValueIndex(self, key, index):
        re = self.conn
        if re.exists(key):
            return re.lrange(key, 0, index)
        else:
            msg = 'no key'
            return msg

    def GetKeyCount(self):
        return self.conn.dbsize()

    def GetRandomKey(self):
        return self.conn.randomkey()

    def SetHashValueByKey(self, key, field, value):
        re = self.conn
        if re.exists(key):
            re.hset(key, field, value)
        else:
            msg = 'no key'
            return msg

    def InsertHashValueByKey(self, key, field, value):
        re = self.conn
        try:
            re.hset(key, field, value)
        except:
            self.logger.debug('insert fail! key:{}, field:{}, value:{}'.format(key, field, value))

    def dictInDictGetValue(self, dict1, obj, default=None):
        for k, v in dict1.items():
            if k == obj:
                return v
            else:
                if type(v) is dict:
                    re = self.dictInDictGetValue(v, obj)
                    if re is not default:
                        return re
    def isMemberExist(self,key,name):
        re = self.conn
        if re.exists(key):
            if re.zrevrank(key,name) is not None:
                return True
            else:
                return False
        else:
            self.logger.debug('No key! key:{}'.format(key))
            return False

    def GetSetMembers(self, key):
        re = self.conn
        if re.exists(key):
            return re.zrevrange(key,0,100)
        else:
            self.logger.debug('No key! key:{}'.format(key))
            return []

    def GetZsetValueByScore(self, key, score_min, score_max):
        re = self.conn
        if re.exists(key):
            return re.zrangebyscore(key, score_min, score_max)
        else:
            self.logger.debug('No key! key:{}'.format(key))
            return []


if __name__ == '__main__':
    redis_client = RedisDb()
    get_va = redis_client.GetZsetValueByScore('16_HSI2006', 1590473488512, 1590473488999)
    print(1)

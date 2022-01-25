# -*- coding: utf-8 -*-
# !/usr/bin/python
# @Author: WX
# @Create Time: 2020/4/16
# @Software: PyCharm

import time
import datetime
from common.basic_info import *
import asyncio
import threading
from pynput import keyboard
from common.test_log.ed_log import get_log
from test_config import *
import xlrd


def excel_to_list(file_name):
    # 从Excel中读取参数
    get_list = []
    workbook = xlrd.open_workbook(file_name)
    sheet = workbook.sheet_by_index(0)
    for row in range(0, sheet.nrows):  # 从第一行开始取值，取到最后一行
        get_list.append(sheet.row_values(row))  # 将每行的数据存入大列表中，每行数据都是一个list
    return get_list


class MyThread(threading.Thread):
    def __init__(self, func, args):
        super(MyThread, self).__init__()
        self.func = func
        self.args = args
        self.result = None

    def run(self):
        self.result = self.func(*self.args)


class KeyboardListen(object):
    def __new__(cls, *args, **kwargs):
        # 单例模式
        if not hasattr(cls, 'instance'):
            cls.instance = super(KeyboardListen, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.key = None
        self.input_num = 0
        if sys.platform == 'win32':
            print('Please wait 10 seconds for keyboard listening to init in windows system.')

    def on_press(self, key):
        pass

    def on_release(self, key):
        try:
            # 因可能输入键不是主键盘信息，则char无值，此时取key.vk值替代
            self.key = key.char
            if self.key == None:
                self.key = str(key.vk)
            self.input_num += 1
        except Exception as e:
            print('Input error, please check: {}'.format(e))
            self.key = None

    def listen(self):
        with keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            listener.join()

    def start_listen(self):
        t1 = MyThread(func=self.listen, args=())
        t1.setDaemon(True)
        t1.start()  # 启动监控线程


class Common(object):
    def __new__(cls, *args, **kwargs):
        # 单例模式
        if not hasattr(cls, 'instance'):
            cls.instance = super(Common, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.logger = get_log()

    def getCurrentDayTimeStampInfo(self):
        now = time.localtime()
        todayBeginTimeStr = '%d.%d.%d_00:00:00' % (now.tm_year, now.tm_mon, now.tm_mday)
        todayBeginTimeStamp = int(time.mktime(time.strptime(todayBeginTimeStr, '%Y.%m.%d_%H:%M:%S')))
        todayEndTimeStamp = todayBeginTimeStamp + 60 * 60 * 24 - 1
        return {'todayBeginTimeStamp': todayBeginTimeStamp, 'todayEndTimeStamp': todayEndTimeStamp}

    def isTimeInToday(self, checkTime):
        currentDayTimeStampInfo = self.getCurrentDayTimeStampInfo()
        todayBeginTimeStamp = currentDayTimeStampInfo['todayBeginTimeStamp']
        todayEndTimeStamp = currentDayTimeStampInfo['todayEndTimeStamp']
        checkTime = int(str(checkTime)[:10])
        if checkTime >= todayBeginTimeStamp and checkTime < todayEndTimeStamp:
            return True
        else:
            return False

    def inToday(self, checkDay):
        today = str(datetime.date.today())
        if checkDay.replace('-0', '-', 2) == today.replace('-0', '-', 2):
            return True
        else:
            return False

    def inYesterday(self, checkDay):
        today = datetime.date.today()
        yesterday = str(today - datetime.timedelta(days=1))
        if checkDay.replace('-0', '-', 2) == yesterday.replace('-0', '-', 2):
            return True
        else:
            return False

    def isTomorrow(self, checkDay):
        today = datetime.date.today()
        yesterday = str(today + datetime.timedelta(days=1))
        if checkDay.replace('-0', '-', 2) == yesterday.replace('-0', '-', 2):
            return True
        else:
            return False

    def getYesterDayStampInfo(self):#为morningstar量身设计的时间校验方法
        today = datetime.date.today()
        yesterday = today - datetime.timedelta(days=1)
        yesterday_start_time = int(time.mktime(time.strptime(str(yesterday), '%Y-%m-%d')))
        yesterday_end_time = (int(time.mktime(time.strptime(str(today), '%Y-%m-%d'))) - 1)
        return {'yesterDayBeginTimeStamp': yesterday_start_time, 'yesterDayEndTimeStamp': yesterday_end_time}

    def isTimeInYesterday(self,checkTime):
        YesterDayStampInfo = self.getYesterDayStampInfo()
        yesterBeginTimeStamp = YesterDayStampInfo['yesterDayBeginTimeStamp']
        yesterEndTimeStamp = YesterDayStampInfo['yesterDayEndTimeStamp']
        checkTime = int(str(checkTime)[:10])
        if checkTime >= yesterBeginTimeStamp and checkTime < yesterEndTimeStamp:
            return True
        else:
            return False

    def getTwelveHourStamp(self):
        today = datetime.date.today()
        todayhour=datetime.datetime(today.year, today.month, today.day, 0, 0, 0)
        twelvehour = todayhour + datetime.timedelta(hours=12)
        twelvehourstamp=int(time.mktime(time.strptime(str(twelvehour), '%Y-%m-%d %H:%M:%S')))
        return twelvehourstamp

    def getNextHKFEStartStamp(self):
        today = datetime.date.today()
        todayhour=datetime.datetime(today.year, today.month, today.day, 0, 0, 0)
        start = todayhour + datetime.timedelta(hours=17, minutes=15)
        todayHKFEStartStamp=int(time.mktime(time.strptime(str(start), '%Y-%m-%d %H:%M:%S')))
        return todayHKFEStartStamp

    def doDicEvaluate(self, dic, key, type=0):
        # type 表示key的类型，0表示整形（如果没找到对应的key则返回0），1表示字符串（如果没找到对应的key则返回''），2表示列表（如果没找到对应的key则返回[]），3表示返回None
        if key in dic.keys():
            return dic[key]
        else:
            if type == 0:
                return 0
            elif type == 1:
                return ''
            elif type == 2:
                return []
            elif type == 3:
                return None

    def searchDicKV(self, dic, keyword):
        if isinstance(dic, dict):
            for x in range(len(dic)):
                temp_key = list(dic.keys())[x]
                temp_value = dic[temp_key]
                if temp_key == keyword:
                    return_value = temp_value
                    return return_value
                return_value = self.searchDicKV(temp_value, keyword)
                if return_value != None:
                    return return_value

    def fixIntNum(self, num, length):
        if str(num).__len__() < length:
            num = '0' + str(num)
            self.fixIntNum(num, length)
        return num

    def isInTradeTime(self, checkTimeStamp, tradeTimeList):
        for timeDic in tradeTimeList:
            start = str(self.fixIntNum(timeDic['start'], 6))
            end = str(self.fixIntNum(timeDic['end'], 6))
            now = time.localtime()
            timeStartStr = '%d.%d.%d_%s' % (now.tm_year, now.tm_mon, now.tm_mday, start)
            timeEndStr = '%d.%d.%d_%s' % (now.tm_year, now.tm_mon, now.tm_mday, end)
            timeStartStamp = int(time.mktime(time.strptime(timeStartStr, '%Y.%m.%d_%H%M%S')))
            timeEndStamp = int(time.mktime(time.strptime(timeEndStr, '%Y.%m.%d_%H%M%S')))
            if checkTimeStamp >= timeStartStamp and checkTimeStamp < timeEndStamp:
                return True
        return False

    def isDataBeforeSubscribe(self, exchange, is_delay, req_source_time, subscribe_time_stamp, tolerance_time=0):
        # 判断数据是否是前数据
        # 毫秒级别对比
        # 外期的source时间比北京时间晚12小时
        if exchange == 'HKFE':      # 港期
            if ((not is_delay) and (int(int(req_source_time) / (pow(10, 6))) < (subscribe_time_stamp + tolerance_time)))\
                or \
                    ((is_delay) and (int(int(req_source_time) / (pow(10, 6))) < (subscribe_time_stamp + tolerance_time - delay_minute * 60 * 1000))):
                return True
        else:       # 外期
            if ((not is_delay) and (int(int(req_source_time) / (pow(10, 6)) + 12 * 60 * 60 * 1000) < (subscribe_time_stamp + tolerance_time))) \
                    or \
                    ((is_delay) and (int(int(req_source_time) / (pow(10, 6)) + 12 * 60 * 60 * 1000) < (subscribe_time_stamp + tolerance_time - delay_minute * 60 * 1000))):
                return True
        return False

    def getFutureLotSizeAndContractMultiplier(self, code):
        futureTypeList = allFuture.keys()
        for futureType in futureTypeList:
            if code in allFuture[futureType]['productInfo'].keys():
                lotSize = allFuture[futureType]['productInfo'][code]['lotSize']
                contractMultiplier = allFuture[futureType]['productInfo'][code]['contractMultiplier']
                return {'lotSize': lotSize, 'contractMultiplier': contractMultiplier}
        return None

    def getNewLoop(self):
        if sys.platform == 'win32':
            new_loop = asyncio.ProactorEventLoop()
        else:
            new_loop = asyncio.new_event_loop()
        return new_loop

    def compareSubData(self, data1, data2):
        # used by delay market subscribing test comparing
        # data2 should be as list type. This function will return if data1 in data2
        data1['commonInfo'].pop('publisherRecvTime')
        data1['commonInfo'].pop('publisherSendTime')
        data1['commonInfo'].pop('collectorRecvTime')
        data1['commonInfo'].pop('collectorSendTime')
        # 如果是静态数据，因可能是采集器写入的update time，则不校验这个字段
        if 'updateTimestamp' in data1.keys():
            data1.pop('updateTimestamp')
        for data_check in data2:
            data_check['commonInfo'].pop('publisherRecvTime')
            data_check['commonInfo'].pop('publisherSendTime')
            data_check['commonInfo'].pop('collectorRecvTime')
            data_check['commonInfo'].pop('collectorSendTime')
            if 'updateTimestamp' in data_check.keys():
                data_check.pop('updateTimestamp')
            if data1 == data_check:
                return True
        self.logger.debug('Subscribe data comparing not match!\ndata1: {}\ndata2: {}'.format(data1, data2))
        return False

    def checkFrequence(self, data_list, frequence):
        record_time = None
        count_num = 0
        if frequence in [0, None]:
            frequence = 1  # 程序默认为1
        for data in data_list:
            if 'tradeTick' in data.keys():
                source_time = int(int(self.searchDicKV(data, 'time')) / pow(10, 9))
            else:
                source_time = int(int(self.searchDicKV(data, 'sourceUpdateTime')) / pow(10, 9))
            if record_time == None:
                record_time = source_time
                count_num = 1
            else:
                if source_time - record_time >= 1:  # 间隔时间大于一秒时
                    if count_num <= frequence + 1:  # 因sourcetime与本地时间可能存在误差，此处加一个误差
                        record_time = source_time
                        count_num = 1
                    else:
                        self.logger.debug('checkFrequence failed:{}'.format(data))
                        return False
                else:
                    count_num += 1
        return True

if __name__ == '__main__':
    now = time.localtime()
    b=Common().inToday('2020-5-20')
    # c = Common().isTimeInYesterday('1589292577343000000')
    print('b1111',b)
    # print(c)

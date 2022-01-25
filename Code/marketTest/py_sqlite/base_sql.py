# -*- coding: utf-8 -*-
# !/usr/bin/python
# @Author: WX
# @Create Time: 2020/4/14
# @Software: PyCharm


import sqlite3
import json
from common.common_method import *
from test_config import *
from common.test_log.ed_log import get_log
from pb_files.quote_type_def_pb2 import *


class SqliteDB(object):
    def __new__(cls, *args, **kwargs):
        # 单例模式
        if not hasattr(cls, 'instance'):
            cls.instance = super(SqliteDB, cls).__new__(cls)
        return cls.instance

    def __init__(self, is_subscribe_record=False):
        self.conn = sqlite3.connect(dbPath, check_same_thread=False)
        self.common = Common()
        self.logger = get_log()
        currentDayTimeStampInfo = self.common.getCurrentDayTimeStampInfo()
        self.todayBeginTimeStamp = currentDayTimeStampInfo['todayBeginTimeStamp']
        self.todayEndTimeStamp = currentDayTimeStampInfo['todayEndTimeStamp']
        self.is_subscribe_record = is_subscribe_record
        self.assemble_num = 100  # sqlite单条插入数值最多为500个
        self.assemble_sql = ''
        self.assemble_float_num = 0
        self.transaction_num = 1  # 为了减少执行sql的次数，此处优化为使用事务一次性批量插入: 此参数表示事务里执行的sql命令个数
        self.transaction_float_num = 0

    def commit(self, sql):
        try:
            cursor = self.conn.cursor()
            cursor.executescript(sql)
            self.conn.commit()
            result = cursor.fetchone()
            return result
        except Exception as e:
            self.logger.debug("sqlCommit exec error: {}".format(e))

    def select(self, sql):
        self.logger.debug('sqlSelect Sql: {}'.format(sql))
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql)
            result = cursor.fetchone()
            return result
        except Exception as e:
            self.logger.debug("sqlSelect exec error: {}".format(e))

    def multi_select(self, sql):
        self.logger.debug('sqlSelectMulil Sql:{}'.format(sql))
        resList = []
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql)
            result = cursor.fetchall()
            for line in result:
                resList.append(line)
            return resList
        except Exception as e:
            self.logger.debug("sqlSelectMulil exec error: {}".format(e))

    def multi_select_with_gen(self, sql):
        self.logger.debug('sqlSelectMulil Sql:{}'.format(sql))
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql)
            result = cursor.fetchall()
            for line in result:
                yield line
        except Exception as e:
            self.logger.debug("sqlSelectMulilWithGen exec error: {}".format(e))

    def exit(self):
        self.conn.close()

    def stress_insert(self, assemble_first, single_info):
        self.assemble_float_num += 1
        self.assemble_sql = self.assemble_sql + single_info
        if self.assemble_float_num >= self.assemble_num:
            single_finaly_sql = (assemble_first + self.assemble_sql).rstrip(', ') + ';\n'
            self.assemble_sql = ''
            self.assemble_float_num = 0
            self.transaction_float_num += 1
            if self.transaction_float_num == 1:
                self.finaly_sql = 'begin;\n' + single_finaly_sql
            elif self.transaction_float_num > 1 and self.transaction_float_num < self.transaction_num:
                self.finaly_sql = self.finaly_sql + single_finaly_sql
            elif self.transaction_float_num > 1 and self.transaction_float_num == self.transaction_num:
                self.finaly_sql = self.finaly_sql + single_finaly_sql + 'commit;'
            if self.transaction_float_num >= self.transaction_num:
                self.commit(self.finaly_sql)
                self.transaction_float_num = 0

# ------------------------------------------------ZMQ start----------------------------------------------------------

    def pub_new_record(self, data_type, origin_info, json_info):
        record_time = int(time.time())
        assemble_first = "insert into %s (data_type, origin_info, json_info, record_time) values " % (
            pub_table)
        single_info = "('%s','%s', '%s', %d), " % (
        data_type, origin_info, str(json_info), record_time)
        self.stress_insert(assemble_first, single_info)

    def get_pub_json_records(self, data_type, request_num=10):
        # 因为逐笔成交数据需要校验成交方向，则取数据按顺序取
        sql = "select json_info, record_time from %s where data_type = '%s' and record_time >= %d and record_time < %d ORDER BY id LIMIT %d;" % (pub_table, data_type, self.todayBeginTimeStamp, self.todayEndTimeStamp, request_num)
        result = self.multi_select(sql)
        return result

    def deal_new_record(self, data_type, origin_info, json_info):
        record_time = int(time.time())
        sql = "insert into %s (data_type, origin_info, json_info, record_time) values ('%s','%s','%s', %d);" %(deal_table, data_type, str(origin_info), str(json_info), record_time)
        self.commit(sql)

    def get_deal_json_records(self, data_type, request_num=10):
        sql = "select json_info, record_time from %s where data_type = '%s' and record_time >= %d and record_time < %d ORDER BY id DESC LIMIT %d;" % (deal_table, data_type, self.todayBeginTimeStamp, self.todayEndTimeStamp, request_num)
        result = self.multi_select(sql)
        return result

# ------------------------------------------------ZMQ end-------------------------------------------------------------

# ------------------------------------------------Websocket start-----------------------------------------------------

    def subscribe_new_record(self, data_type, instr_code, source_update_time, json_info):
        if self.is_subscribe_record:
            json_info = json.dumps(json_info)
            record_time = int(time.time() * 1000)  # 毫秒级
            assemble_first = "insert into %s (data_type, instr_code, source_update_time, record_time, json_info) values " % (subscribe_table)
            single_info = "('%s','%s', '%s', %d, '%s'), " % (data_type, instr_code, str(source_update_time), record_time, str(json_info))
            self.stress_insert(assemble_first, single_info)
        else:
            pass

    # 将品种交易状态入库
    def trade_status_record(self, data_type, product_code, time_stamp, json_info):
        # json_info = json.dumps(json_info)
        record_time = int(time.time() * 1000)  # 毫秒级
        sql = "insert into %s (data_type, product_code, source_update_time, record_time, json_info) values ('%s','%s', '%s', %d, '%s')" % (
            subscribe_table, data_type, product_code, str(time_stamp), record_time, str(json_info))
        result = self.multi_select(sql)
        return result

    def get_subscribe_record(self, instr_code, data_type, source_update_time):
        # return list records
        if data_type != QuoteMsgType.PUSH_BASIC:
            sql = "select json_info from %s where instr_code = '%s' and data_type = %s and source_update_time = %s ORDER BY id DESC;" % (subscribe_table, str(instr_code), str(data_type), str(source_update_time))
        else:
            # 如果是静态数据，因可能是采集器写入的update time，则不根据这个进行查询
            sql = "select json_info from %s where instr_code = '%s' and data_type = %s ORDER BY id DESC;" % (
                subscribe_table, str(instr_code), str(data_type))

        resultList = self.multi_select(sql)
        self.logger.debug("get_subscribe_record:{}".format(resultList))
        json_result_list = []
        for result in resultList:
            json_result = json.loads(result[0])
            json_result_list.append(json_result)
        return json_result_list
# ------------------------------------------------Websocket end-----------------------------------------------------

# ------------------------------------------------Analysis start-----------------------------------------------------

    def insert_time_analysis_info(self, exchange, product_code, instr_code, data_type, collect2out, subscribe2out, collector2subscribe, source2collector, inner_total_time, json_info):
        json_info = json.dumps(json_info)
        assemble_first = "insert into %s (exchange, product_code, instr_code, data_type, collect2out, subscribe2out, collector2subscribe, source2collector, inner_total_time, json_info) values " % (
            time_analysis_base_table)
        single_info = "('%s','%s', '%s', %d, '%d', '%d', '%d', '%d', '%d', '%s'), " % (
        exchange, product_code, instr_code, data_type, collect2out, subscribe2out, collector2subscribe, source2collector, inner_total_time, str(json_info))
        self.stress_insert(assemble_first, single_info)

    def get_all_info(self):
        get_data_num_sql = "select id from %s order by id desc limit 1;" % time_analysis_base_table     # count(*) 查询太慢
        data_num = self.select(get_data_num_sql)[0]
        gen_list = []
        # 为避免取sqlite数据时内存溢出，一次最多取100w条
        per_num = 100 * 10000
        max_round = int(data_num / per_num) + 1
        for i in range(max_round):
            get_infos_sql = ''
            if i != max_round - 1:
                get_infos_sql = "select exchange, product_code, instr_code, data_type, collect2out, subscribe2out, collector2subscribe, source2collector, inner_total_time, json_info from %s limit %d, %d;" % (time_analysis_base_table, i * per_num, per_num)
            elif i == max_round - 1:
                get_infos_sql = "select exchange, product_code, instr_code, data_type, collect2out, subscribe2out, collector2subscribe, source2collector, inner_total_time, json_info from %s limit %d, -1;" % (
                time_analysis_base_table, i * per_num)
            gen_results = self.multi_select_with_gen(get_infos_sql)
            gen_list.append(iter(gen_results))
        return gen_list

    def get_instr_info(self, instr_code):
        get_data_num_sql = "select count(*) from %s where instr_code='%s';" % (time_analysis_base_table, instr_code)
        data_num = self.select(get_data_num_sql)[0]
        gen_list = []
        # 为避免取sqlite数据时内存溢出，一次最多取100w条
        per_num = 100 * 10000
        max_round = int(data_num / per_num) + 1
        for i in range(max_round):
            get_infos_sql = ''
            if i != max_round - 1:
                get_infos_sql = "select exchange, product_code, instr_code, data_type, collect2out, subscribe2out, collector2subscribe, source2collector, inner_total_time, json_info from %s where instr_code='%s' limit %d, %d;" % (
                    time_analysis_base_table, instr_code, i * per_num, per_num)
            elif i == max_round - 1:
                get_infos_sql = "select exchange, product_code, instr_code, data_type, collect2out, subscribe2out, collector2subscribe, source2collector, inner_total_time, json_info from %s where instr_code='%s' limit %d, -1;" % (
                    time_analysis_base_table, instr_code, i * per_num)
            gen_results = self.multi_select_with_gen(get_infos_sql)
            gen_list.append(iter(gen_results))
        return gen_list

    def get_all_instr_code(self):
        sql = 'select instr_code from %s;' % time_analysis_base_table
        results = self.multi_select(sql)
        instr_list = []
        for result in results:
            instr_list.append(result[0])
        return list(set(instr_list))

    def insert_statistical_analysis(self, desc, exchange, product_code, instr_code, data_type, max_collect2out, min_collect2out, av_collect2out, max_subscribe2out, min_subscribe2out, av_subscribe2out, max_collector2subscribe, min_collector2subscribe, av_collector2subscribe, max_source2collector, min_source2collector, av_source2collector, max_inner_total_time, min_inner_total_time, av_inner_total_time, analysis_num):
        sql = "insert into %s ('desc', exchange, product_code, instr_code, data_type, max_collect2out, min_collect2out, av_collect2out, max_subscribe2out, min_subscribe2out, av_subscribe2out, max_collector2subscribe, min_collector2subscribe, av_collector2subscribe, max_source2collector, min_source2collector, av_source2collector, max_inner_total_time, min_inner_total_time, av_inner_total_time, analysis_num) values ( '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%d');" % (
        statistical_analysis_table, desc, exchange, product_code, instr_code, data_type, max_collect2out, min_collect2out, av_collect2out, max_subscribe2out, min_subscribe2out, av_subscribe2out, max_collector2subscribe, min_collector2subscribe, av_collector2subscribe, max_source2collector, min_source2collector, av_source2collector, max_inner_total_time, min_inner_total_time, av_inner_total_time, analysis_num)
        self.commit(sql)

# ------------------------------------------------Analysis end-----------------------------------------------------

# -------------------------------------------------------Calculate------------------------------------------------------
    def cal_insert_tick(self, data_type, product_code, instr_code, precision, price, vol, time):
        if precision is None:
            precision = 0
        assemble_first = "insert into %s (data_type, product_code, instr_code, precision, price, vol, time) values " % (
            cal_table)
        single_info = "('%s','%s', '%s', '%d', '%d', '%d', '%d')," % (data_type, product_code, instr_code, precision, price, vol, time)
        self.stress_insert(assemble_first, single_info)

    def cal_get_tick(self, instr_code, start_time, end_time):
        # 传入时间请传毫秒级别
        sql = "select instr_code, precision, max(price), min(price), sum(vol), avg(price) from %s where instr_code = '%s' and time >= %s and time < %s;" % (
            cal_table, str(instr_code), str(start_time), str(end_time))
        data_base = self.select(sql)
        max_price = data_base[2]
        min_price = data_base[3]
        sum_vol = data_base[4]
        av_price =data_base[5]
        precision = data_base[1]
        sql = "select price from %s where instr_code = '%s' and time >= %s order by id limit 1;" % (
            cal_table, str(instr_code), str(start_time))
        open_price = self.select(sql)[0]
        sql = "select price from %s where instr_code = '%s' and time < %s order by id desc limit 1;" % (
            cal_table, str(instr_code), str(end_time))
        close_price = self.select(sql)[0]
        return_dic = {}
        return_dic['max_price'] = max_price
        return_dic['min_price'] = min_price
        return_dic['open_price'] = open_price
        return_dic['close_price'] = close_price
        return_dic['av_price'] = av_price
        return_dic['sum_vol'] = sum_vol
        return_dic['precision'] = precision
        return return_dic




if __name__ == '__main__':
    sq = SqliteDB()
    ret = sq.get_all_info()
    for gen in ret:
        for info in gen:
            print(info)
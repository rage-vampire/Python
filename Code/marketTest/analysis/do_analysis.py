# -*- coding: utf-8 -*-
# !/usr/bin/python
# @Author: WX
# @Create Time: 2020/5/28
# @Software: PyCharm

from common.common_method import Common
from py_sqlite.base_sql import SqliteDB
import json
import time
import re
from matplotlib import pyplot as plt
from matplotlib.font_manager import FontProperties


class Analysis(object):
    def __init__(self):
        self.common = Common()
        self.sq = SqliteDB()
        self.my_font = FontProperties(fname='/usr/share/fonts/cjkuni-uming/uming.ttc')

    def tryint(self, s):          # 将元素中的数字转换为int后再排序
        try:
            return int(s)
        except ValueError:
            return s

    def str2int(self, v_str):     # 将元素中的字符串和数字分割开
        return [self.tryint(sub_str) for sub_str in re.split('([0-9]+)', v_str)]

    def sort_humanly(self, v_list):       # 以分割后的list为单位进行排序
        return sorted(v_list, key=self.str2int)


    def statistical_func(self, info_gen_list):
        analysis_num = 0
        sum_collect2out = 0.0
        sum_subscribe2out = 0.0
        sum_collector2subscribe = 0.0
        sum_source2collector = 0.0
        sum_inner_total_time = 0.0
        max_collect2out = 0.0
        max_subscribe2out = 0.0
        max_collector2subscribe = 0.0
        max_source2collector = 0.0
        max_inner_total_time = 0.0
        min_collect2out = 999999.9
        min_subscribe2out = 999999.9
        min_collector2subscribe = 999999.9
        min_source2collector = 999999.9
        min_inner_total_time = 999999.9
        exchange_list = []
        product_code_list = []
        instr_code_list = []
        data_type_list = []
        plot_info = {}
        for single_gen in info_gen_list:
            for info in single_gen:
                analysis_num += 1
                json_info = json.loads(info[9])
                try:
                    exchange = info[0]
                    product_code = info[1]
                    instr_code = info[2]
                    data_type = info[3]
                    exchange_list.append(exchange)
                    product_code_list.append(product_code)
                    instr_code_list.append(instr_code)
                    data_type_list.append(data_type)
                    # 去重
                    exchange_list = list(set(exchange_list))
                    product_code_list = list(set(product_code_list))
                    instr_code_list = list(set(instr_code_list))
                    data_type_list = list(set(data_type_list))

                    collect2out = info[4]
                    subscribe2out = info[5]
                    collector2subscribe = info[6]
                    source2collector = info[7]
                    inner_total_time = info[8]

                    sum_collect2out += collect2out
                    sum_subscribe2out += subscribe2out
                    sum_collector2subscribe += collector2subscribe
                    sum_source2collector += source2collector
                    sum_inner_total_time += inner_total_time
                    max_collect2out = max(max_collect2out, collect2out)
                    max_subscribe2out = max(max_subscribe2out, subscribe2out)
                    max_collector2subscribe = max(max_collector2subscribe, collector2subscribe)
                    max_source2collector = max(max_source2collector, source2collector)
                    max_inner_total_time = max(max_inner_total_time, inner_total_time)
                    min_collect2out = min(min_collect2out, collect2out)
                    min_subscribe2out = min(min_subscribe2out, subscribe2out)
                    min_collector2subscribe = min(min_collector2subscribe, collector2subscribe)
                    min_source2collector = min(min_source2collector, source2collector)
                    min_inner_total_time = min(min_inner_total_time, inner_total_time)

                    int_inner_total_time = int(inner_total_time)
                    if 'inner_total_time_' + str(int_inner_total_time) not in plot_info.keys():
                        plot_info['inner_total_time_' + str(int_inner_total_time)] = 1
                    else:
                        plot_info['inner_total_time_' + str(int_inner_total_time)] += 1
                except Exception as e:
                    self.common.logger.debug('Analysis error:{}\nJsonInfo:{}'.format(e, json_info))

        av_collect2out = round(sum_collect2out / analysis_num, 2)
        av_subscribe2out = round(sum_subscribe2out / analysis_num, 2)
        av_collector2subscribe = round(sum_collector2subscribe / analysis_num, 2)
        av_source2collector = round(sum_source2collector / analysis_num, 2)
        av_inner_total_time = round(sum_inner_total_time / analysis_num, 2)
        results = {}
        results['max_collect2out'] = max_collect2out
        results['min_collect2out'] = min_collect2out
        results['av_collect2out'] = av_collect2out
        results['max_subscribe2out'] = max_subscribe2out
        results['min_subscribe2out'] = min_subscribe2out
        results['av_subscribe2out'] = av_subscribe2out
        results['max_collector2subscribe'] = max_collector2subscribe
        results['min_collector2subscribe'] = min_collector2subscribe
        results['av_collector2subscribe'] = av_collector2subscribe
        results['max_source2collector'] = max_source2collector
        results['min_source2collector'] = min_source2collector
        results['av_source2collector'] = av_source2collector
        results['max_inner_total_time'] = max_inner_total_time
        results['min_inner_total_time'] = min_inner_total_time
        results['av_inner_total_time'] = av_inner_total_time
        results['analysis_num'] = analysis_num
        results['exchange_list'] = exchange_list
        results['product_code_list'] = product_code_list
        results['instr_code_list'] = instr_code_list
        results['data_type_list'] = data_type_list
        plot_info['inner_av_time'] = av_inner_total_time
        plot_info['inner_max_time'] = max_inner_total_time
        plot_info['inner_min_time'] = min_inner_total_time
        plot_info['analysis_num'] = analysis_num
        results['plot_info'] = plot_info
        return results

    def plot_pic(self, plot_info, pic_name=None):
        x_inner_list = []
        y_inner_list = []
        analysis_num = plot_info['analysis_num']
        sum_num, get_90per_time, get_95per_time, get_99per_time, get_below_10ms_num = 0, 0.0, 0.0, 0.0, 0
        for key in self.sort_humanly(plot_info.keys()):
            if 'inner_total_time_' in key:
                x_inner = int(re.findall('\d+', key)[-1])
                y_inner = plot_info[key]
                x_inner_list.append(x_inner)
                y_inner_list.append(y_inner)
                sum_num += y_inner
                if get_90per_time == 0.0 and sum_num >= 0.9 * analysis_num:
                    get_90per_time = x_inner
                if get_95per_time == 0.0 and sum_num >= 0.95 * analysis_num:
                    get_95per_time = x_inner
                if get_99per_time == 0.0 and sum_num >= 0.99 * analysis_num:
                    get_99per_time = x_inner
                if x_inner <= 10:
                    get_below_10ms_num += y_inner

        x_min = plot_info['inner_min_time']
        x_max = plot_info['inner_max_time']
        x_av = plot_info['inner_av_time']
        per_of_below_10ms = round(get_below_10ms_num / analysis_num, 4)
        print(get_below_10ms_num / analysis_num)
        plt.figure(figsize=(30, 10), dpi=80)    # 设置画布大小
        xticks_gap = 5    # 设置刻度间距
        xticks = [i for i in range(0, x_max + xticks_gap, xticks_gap)]
        plt.xticks(xticks, rotation=90)  # 设置刻度
        plot_info.pop('analysis_num')
        max_times = max(list(plot_info.values()))
        plt.axis([0, 1.01 * x_max, 0, 1.01 * max_times])
        plt.scatter(x_inner_list, y_inner_list, color='blue', label='Inner cost time')  # 散点图
        plt.grid(alpha=0.4, ls='--')    # 网格线设置
        plt.axvline(x_av, color='green', label='Average time for inner cost')
        plt.annotate(' Average cost time is ' + str(x_av) + 'ms', (x_av, 120000), color='green')
        plt.axvline(get_90per_time, color='c', label='90% data\'s time is equal or below this line')
        plt.annotate(' 90% data\'s time is equal or below '+str(get_90per_time) + 'ms', (get_90per_time, 20000), color='c')
        plt.axvline(get_95per_time, color='m', label='95% data\'s time is equal or below this line')
        plt.annotate(' 95% data\'s time is equal or below '+str(get_95per_time) + 'ms', (get_95per_time, 40000), color='m')
        plt.axvline(get_99per_time, color='r', label='99% data\'s time is equal or below this line')
        plt.annotate(' 99% data\'s time is equal or below '+str(get_99per_time) + 'ms', (get_99per_time, 60000), color='r')
        plt.axvline(10, color='y', label='10 ms time')
        plt.annotate(' {}% data\'s time is equal or below 10ms'.format(per_of_below_10ms * 100), (10, 200000), color='y')
        plt.xlabel('内部耗时(ms)', fontproperties=self.my_font, fontsize=18)
        plt.ylabel('出现次数', fontproperties=self.my_font, fontsize=18)
        plt.title('内部程序耗时分布图(样本数: %d)' % (analysis_num), fontproperties=self.my_font, fontsize=18)
        plt.legend()
        if pic_name:
            plt.savefig('./{}'.format(pic_name))
        plt.show()

    def all_cost(self):
            desc = 'analysis_all'
            info_gen_list = self.sq.get_all_info()
            results = self.statistical_func(info_gen_list)
            max_collect2out = results['max_collect2out']
            min_collect2out = results['min_collect2out']
            av_collect2out = results['av_collect2out']
            max_subscribe2out = results['max_subscribe2out']
            min_subscribe2out = results['min_subscribe2out']
            av_subscribe2out = results['av_subscribe2out']
            max_collector2subscribe = results['max_collector2subscribe']
            min_collector2subscribe = results['min_collector2subscribe']
            av_collector2subscribe = results['av_collector2subscribe']
            max_source2collector = results['max_source2collector']
            min_source2collector = results['min_source2collector']
            av_source2collector = results['av_source2collector']
            max_inner_total_time = results['max_inner_total_time']
            min_inner_total_time = results['min_inner_total_time']
            av_inner_total_time = results['av_inner_total_time']
            analysis_num = results['analysis_num']
            plot_info = results['plot_info']
            self.sq.insert_statistical_analysis(desc, 'all', 'all', 'all', 'all', max_collect2out, min_collect2out, av_collect2out, max_subscribe2out, min_subscribe2out, av_subscribe2out, max_collector2subscribe, min_collector2subscribe, av_collector2subscribe, max_source2collector, min_source2collector, av_source2collector, max_inner_total_time, min_inner_total_time, av_inner_total_time, analysis_num)
            self.plot_pic(plot_info, './all.svg')

    def different_instr_cost(self):
        instr_list = self.sq.get_all_instr_code()
        for instr_code in instr_list:
            desc = 'single instr cost time'
            info_gen_list = self.sq.get_instr_info(instr_code)
            results = self.statistical_func(info_gen_list)
            max_collect2out = results['max_collect2out']
            min_collect2out = results['min_collect2out']
            av_collect2out = results['av_collect2out']
            max_subscribe2out = results['max_subscribe2out']
            min_subscribe2out = results['min_subscribe2out']
            av_subscribe2out = results['av_subscribe2out']
            max_collector2subscribe = results['max_collector2subscribe']
            min_collector2subscribe = results['min_collector2subscribe']
            av_collector2subscribe = results['av_collector2subscribe']
            max_source2collector = results['max_source2collector']
            min_source2collector = results['min_source2collector']
            av_source2collector = results['av_source2collector']
            max_inner_total_time = results['max_inner_total_time']
            min_inner_total_time = results['min_inner_total_time']
            av_inner_total_time = results['av_inner_total_time']
            analysis_num = results['analysis_num']
            exchange = results['exchange_list'][0]
            product_code = results['product_code_list'][0]
            data_type = 'all'
            self.sq.insert_statistical_analysis(desc, exchange, product_code, instr_code, data_type, max_collect2out, min_collect2out, av_collect2out, max_subscribe2out, min_subscribe2out, av_subscribe2out, max_collector2subscribe, min_collector2subscribe, av_collector2subscribe, max_source2collector, min_source2collector, av_source2collector, max_inner_total_time, min_inner_total_time, av_inner_total_time, analysis_num)


if __name__ == '__main__':
    start = time.time()
    analysis = Analysis()
    analysis.all_cost()
    # analysis.different_instr_cost()
    print('analysis cost time', time.time() - start)
# -*- coding: utf-8 -*-
# @Date : 2021/7/22 15:23
# @File : dump_pcap_data.py
# @Author : Lizi


import pyshark
import re


# pkts = rdpcap('ors_tgw_bond0_90(1).cap')

class Dump_Data:
    dump_data_list = []
    dump_timestamp = []

    def __init__(self):
        """指定ORS和TGW的IP地址"""
        self.ors_ip = '10.60.43.101'
        self.tgw_ip = '10.60.43.200'

    def data_data_dump(self):
        cap = pyshark.FileCapture('../data_file/zhanbao.pcap')
        new_order_len = 121              # 新订单去除头部的长度
        order_confirm_len = 201          # 委托确认/撤单成功响应去除头部的长度
        cancel_order_len = 98            # 撤单请求去除头部的长度
        cancel_order_failed_len = 127    # 撤单失败响应成功去除头部的长度
        match_order_len = 165            # 委托成交去除头部长度
        for i in cap:
            if 'data' in i:     # 判断i里面是否有data数据
                len_data = len(i.data.data)
                if i.ip.src_host == self.ors_ip and i.ip.dst_host == self.tgw_ip:    # 指定源IP地址和目标ip地址
                    """新订单：ORS->TGW"""
                    if len_data % (2 * new_order_len) == 0:    # 新订单
                        count = 0
                        multi = int(len_data / (2 * new_order_len))
                        while count < multi:
                            self.dump_data_list.append(i.data.data[count * (2 * new_order_len):(2 * new_order_len) * (count + 1)])
                            self.dump_timestamp.append(i.sniff_timestamp)
                            count += 1

                elif i.ip.src_host == self.tgw_ip and i.ip.dst_host == self.ors_ip:
                    """委托确认和撤单成功响应：TGW->ORS"""
                    if len_data % (2 * order_confirm_len) == 0:      # 委托确认和撤单成功响应
                        count = 0
                        multi = int(len_data / (2 * order_confirm_len))
                        while count < multi:
                            self.dump_data_list.append(
                                i.data.data[count * (2 * order_confirm_len):(2 * order_confirm_len) * (count + 1)])
                            self.dump_timestamp.append(i.sniff_timestamp)
                            count += 1

                    elif len_data % (2 * cancel_order_len) == 0:       # 撤单请求
                        """撤单请求：TGW->ORS"""
                        print(len_data)
                        count = 0
                        multi = int(len_data / (2 * cancel_order_len))
                        while count < multi:
                            self.dump_data_list.append(
                                i.data.data[count * (2 * cancel_order_len):(2 * cancel_order_len) * (count + 1)])
                            self.dump_timestamp.append(i.sniff_timestamp)
                            count += 1

                    elif len_data % (2 * cancel_order_failed_len) == 0:          # 撤单失败响应
                        """撤单响应失败：TGW->ORS"""
                        count = 0
                        multi = int(len_data / (2 * cancel_order_failed_len))
                        while count < multi:
                            self.dump_data_list.append(
                                i.data.data[
                                count * (2 * cancel_order_failed_len):(2 * cancel_order_failed_len) * (count + 1)])
                            self.dump_timestamp.append(i.sniff_timestamp)
                            count += 1

                    elif len_data % (2 * match_order_len) == 0:            # 委托成交
                        """委托成交：TGW->ORS"""
                        count = 0
                        multi = int(len_data / (2 * match_order_len))
                        while count < multi:
                            self.dump_data_list.append(
                                i.data.data[count * (2 * match_order_len):(2 * match_order_len) * (count + 1)])
                            self.dump_timestamp.append(i.sniff_timestamp)
                            count += 1
                else:
                    continue
            else:
                continue
        # print(self.dump_data)
        # print(self.dump_timestamp)

        cap.close()

    def data_data_dump1(self):
        cap = pyshark.FileCapture('../data_file/zhanbao.pcap')
        new_order_len = 2 * 121  # 新订单去除头部的长度
        order_confirm_len = 2 * 201  # 委托确认/撤单成功响应去除头部的长度
        cancel_order_len = 2 * 98  # 撤单请求去除头部的长度
        cancel_order_failed_len = 2 * 127  # 撤单失败响应成功去除头部的长度
        match_order_len = 2 * 165  # 委托成交去除头部长度
        dump_data_list = []
        pos = 0
        all_data_list = []

        for i in cap:
            if 'data' in i:  # 判断i里面是否有data数据
                tmp_list = None

                dump_data_list.append(i.data.data)
                dump_data_str = ''.join(dump_data_list)

                msg_type = dump_data_str[pos:pos + 8]
                int_msg_type = int(str(msg_type), 16)
                re_new_order = re.match(r'1\d{3}01', str(int_msg_type))
                re_order_cofirm = re.match(r'2\d{3}02', str(int_msg_type))
                re_order_match = re.match(r'2\d{3}15', str(int_msg_type))

                if re_new_order is not None:
                    # tmp_list.append(dump_data_str[pos:pos+new_order_len])
                    tmp_list = dump_data_str[pos:pos + new_order_len]
                    pos += new_order_len

                elif re_order_cofirm is not None:
                    # tmp_list.append(dump_data_str[pos:pos+order_confirm_len])
                    tmp_list = dump_data_str[pos:pos + order_confirm_len]
                    pos += order_confirm_len

                elif int_msg_type == 190007:
                    # tmp_list.append(dump_data_str[pos:pos+cancel_order_len])
                    tmp_list = dump_data_str[pos:pos + cancel_order_len]
                    pos += cancel_order_len

                elif int_msg_type == 290008:
                    # tmp_list.append(dump_data_str[pos:pos+cancel_order_failed_len])
                    tmp_list = dump_data_str[pos:pos + cancel_order_failed_len]
                    pos += cancel_order_failed_len

                elif re_order_match is not None:
                    # tmp_list.append(dump_data_str[pos:pos+match_order_len])
                    tmp_list = dump_data_str[pos:pos + match_order_len]
                    pos += match_order_len
                else:
                    continue
        print(all_data_list)
        cap.close()


# if __name__ == '__main__':
    # dump = Dump_Data('196.168.0.90', '196.168.0.81')
dump = Dump_Data()
dump.data_data_dump()

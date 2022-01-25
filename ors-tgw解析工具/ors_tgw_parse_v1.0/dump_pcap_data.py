# -*- coding: utf-8 -*-
# @Date : 2021/7/22 15:23
# @File : dump_pcap_data.py
# @Author : Lizi
import time

import pyshark
import re
import os

print(os.getcwd())



class Dump_Data:
    dump_timestamp = []  # 用于存放时间戳
    all_data_list = []  # 用于存放data数据
    src_ip_list = []  # 存放包源IP地址
    dst_ip_list = []  # 存放包目标IP地址
    src_port_list = []  # 存放包源端口号
    dst_port_list = []  # 存放包目标端口号
    file_path = ''

    def __init__(self, ors_ip, tgw_ip, ors_port, tgw_port,fpath):
        """指定ORS和TGW的IP地址"""
        self.ors_ip = ors_ip
        self.tgw_ip = tgw_ip
        self.ors_port = ors_port
        self.tgw_port = tgw_port
        self.file_path = fpath

    def data_parse(self, src_ip, dst_ip, src_port, dst_port, tmpdata, timestamp):
        new_order_len = 2 * 121  # 新订单去除头部的长度
        order_confirm_len = 2 * 201  # 委托确认/撤单成功响应去除头部的长度
        cancel_order_len = 2 * 98  # 撤单请求去除头部的长度
        cancel_order_failed_len = 2 * 127  # 撤单失败响应成功去除头部的长度
        match_order_len = 2 * 165  # 委托成交去除头部长度
        temp_str = ''

        pre_pos = 0  # 用于定位msgtype开始位置
        pos = 0
        flag = True
        flag_2 = 0
        while flag:
            '''根据msgtype正则判断订单的类型'''
            msg_type = tmpdata[pos:pos + 8]
            tmp_msg_type = int(str(msg_type), 16)

            re_all = re.match(r'[1,2]\d{3}[0,1][1,2,5,7,8]', str(tmp_msg_type))
            if re_all is not None and len(msg_type) == 8:
                flag_2 = 1
                int_msg_type = int(str(msg_type), 16)
                re_new_order = re.match(r'1\d{3}01', str(int_msg_type))
                re_order_cofirm = re.match(r'2\d{3}02', str(int_msg_type))
                re_order_match = re.match(r'2\d{3}15', str(int_msg_type))

                if re_new_order is not None:
                    """新订单"""
                    self.all_data_list.append(
                        tmpdata[pos:pos + new_order_len])  # 获取data值，如果出现粘包的情况，则pos偏移data长度，继续获取data的值
                    self.dump_timestamp.append(timestamp)
                    self.src_ip_list.append(src_ip)
                    self.dst_ip_list.append(dst_ip)
                    self.src_port_list.append(src_port)
                    self.dst_port_list.append(dst_port)
                    temp_str += tmpdata[pos:pos + new_order_len]
                    pre_pos = pos
                    pos += new_order_len
                    if len(temp_str) == len(tmpdata):  # 当新的字符串的长度等于原tmpdata长度则退出
                        flag = False

                elif re_order_cofirm is not None:
                    """委托确认/撤单响应"""
                    self.all_data_list.append(tmpdata[pos:pos + order_confirm_len])
                    self.dump_timestamp.append(timestamp)
                    self.src_ip_list.append(src_ip)
                    self.dst_ip_list.append(dst_ip)
                    self.src_port_list.append(src_port)
                    self.dst_port_list.append(dst_port)
                    temp_str += tmpdata[pos:pos + order_confirm_len]
                    pre_pos = pos
                    pos += order_confirm_len
                    if len(temp_str) == len(tmpdata):
                        flag = False

                elif int_msg_type == 190007:
                    '''撤单请求'''
                    self.all_data_list.append(tmpdata[pos:pos + cancel_order_len])
                    self.dump_timestamp.append(timestamp)
                    self.src_ip_list.append(src_ip)
                    self.dst_ip_list.append(dst_ip)
                    self.src_port_list.append(src_port)
                    self.dst_port_list.append(dst_port)
                    temp_str += tmpdata[pos:pos + cancel_order_len]
                    pre_pos = pos
                    pos += cancel_order_len
                    if len(temp_str) == len(tmpdata):
                        flag = False

                elif int_msg_type == 290008:
                    """撤单失败响应"""
                    self.all_data_list.append(tmpdata[pos:pos + cancel_order_failed_len])
                    self.dump_timestamp.append(timestamp)
                    self.src_ip_list.append(src_ip)
                    self.dst_ip_list.append(dst_ip)
                    self.src_port_list.append(src_port)
                    self.dst_port_list.append(dst_port)
                    temp_str += tmpdata[pos:pos + cancel_order_failed_len]
                    pre_pos = pos
                    pos += cancel_order_failed_len
                    if len(temp_str) == len(tmpdata):
                        flag = False

                elif re_order_match is not None:
                    """委托成交"""
                    self.all_data_list.append(tmpdata[pos:pos + match_order_len])
                    self.dump_timestamp.append(timestamp)
                    self.src_ip_list.append(src_ip)
                    self.dst_ip_list.append(dst_ip)
                    self.src_port_list.append(src_port)
                    self.dst_port_list.append(dst_port)
                    temp_str += tmpdata[pos:pos + match_order_len]
                    pre_pos = pos
                    pos += match_order_len
                    if len(temp_str) == len(tmpdata):
                        flag = False
                else:
                    flag = False

            elif flag_2 == 1:
                slices = pre_pos + 8
                for n in range(slices, len(tmpdata) + 1):
                    tmp_msg_type = int(str(tmpdata[n:n + 8]), 16)
                    temp_re = re.match(r'[1,2]\d{3}[0,1][1,2,5,7,8]', str(tmp_msg_type))
                    if temp_re is not None and len(tmpdata[n:n + 8]) == 8:
                        pos = n
                        temp_str = tmpdata[0:pos]
                        self.all_data_list.pop()
                        self.dump_timestamp.pop()
                        self.src_ip_list.pop()
                        self.dst_ip_list.pop()
                        self.src_port_list.pop()
                        self.dst_port_list.pop()
                        break
            else:
                break

    def data_data_dump(self):
        cap = pyshark.FileCapture(self.file_path)
        sendFlag = 0
        recvFlag = 0
        sendData = ""
        recvData = ""
        count = 0

        for i in cap:  # i是一个数据包
            count += 1
            # print(count)
            if 'data' in i:  # 判断i里面是否有data层
                lay = i.layers[3:]  # i.layers是一个由各层组成列表，[3:]获取DATA层，可能存在多个DATA层
                for j in lay:  # 获取所有DATA层
                    if hasattr(j, 'data'):  # 判断DATA是否有data属性
                        data = j.data
                        # print(data)

                        """根据IP地址和端口号过滤是接受数据还是发送数据"""
                        if i.ip.src_host == self.ors_ip and i.ip.dst_host == self.tgw_ip and i.tcp.srcport == self.ors_port and i.tcp.dstport == self.tgw_port:
                            if sendFlag == 0:  # sendFlag == 0
                                if len(data) >= 2896:  # 如果data数据长度（不包含头）超过2896，则会出现半包的情况，需要和下一条数据进行拼接
                                    sendFlag = 1
                                    sendData = sendData + data
                                    continue
                                else:
                                    sendData = data
                                    temp_timestamp = i.sniff_timestamp
                                    self.data_parse(i.ip.src_host, i.ip.dst_host, i.tcp.srcport, i.tcp.dstport,
                                                    sendData,
                                                    temp_timestamp)
                                    sendData = ""
                            else:
                                if len(data) >= 2896:
                                    sendData = sendData + data
                                    continue
                                else:
                                    sendFlag = 0
                                    sendData = sendData + data
                                    temp_timestamp = i.sniff_timestamp
                                    self.data_parse(i.ip.src_host, i.ip.dst_host, i.tcp.srcport, i.tcp.dstport,
                                                    sendData,
                                                    temp_timestamp)
                                    sendData = ""

                        elif i.tcp.srcport == self.tgw_port and i.tcp.dstport == self.ors_port and i.ip.src_host == self.tgw_ip and i.ip.dst_host == self.ors_ip:
                            if recvFlag == 0:
                                if len(data) >= 2896:
                                    recvFlag = 1
                                    recvData = recvData + data
                                    continue
                                else:
                                    recvData = data
                                    temp_timestamp = i.sniff_timestamp
                                    self.data_parse(i.ip.src_host, i.ip.dst_host, i.tcp.srcport, i.tcp.dstport,
                                                    recvData,
                                                    temp_timestamp)
                                    recvData = ""
                            else:
                                if len(data) >= 2896:
                                    recvData = recvData + data
                                    continue
                                else:
                                    recvFlag = 0
                                    recvData = recvData + data
                                    temp_timestamp = i.sniff_timestamp
                                    self.data_parse(i.ip.src_host, i.ip.dst_host, i.tcp.srcport, i.tcp.dstport,
                                                    recvData,
                                                    temp_timestamp)
                                    recvData = ""
                        else:
                            continue
        cap.close()

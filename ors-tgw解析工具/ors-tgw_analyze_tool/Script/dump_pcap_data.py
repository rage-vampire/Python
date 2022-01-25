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
    file_path = '../data_file/tgwhost_local.pcap'

    def __init__(self, ors_ip, tgw_ip, ors_port, tgw_port):
        """指定ORS和TGW的IP地址"""
        self.ors_ip = ors_ip
        self.tgw_ip = tgw_ip
        self.ors_port = ors_port
        self.tgw_port = tgw_port

    def data_parse(self, src_ip, dst_ip, src_port, dst_port, tempdata, timestamp):
        """
        1、将粘包的数据拆分成单笔数据，存放在all_data_list列表中，all_data_list是由每笔委托为一个元素组成的列表
        2、所有粘包的数据的都是同一时间
        """
        new_order_len = 2 * 121  # 新订单去除头部的长度
        order_confirm_len = 2 * 201  # 委托确认/撤单成功响应去除头部的长度
        cancel_order_len = 2 * 98  # 撤单请求去除头部的长度
        cancel_order_failed_len = 2 * 127  # 撤单失败响应成功去除头部的长度
        match_order_len = 2 * 165  # 委托成交去除头部长度
        temp_str = ''

        pre_pos = 0  # 当出现不完整的半包情况时，记录上一个msgtype的位置
        pos = 0      # 用于定位msgtype开始位置
        flag = True
        flag_2 = 0
        while flag:
            '''根据msgtype正则判断订单的类型'''
            msg_type = tempdata[pos:pos + 8]
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
                        tempdata[pos:pos + new_order_len])  # 获取data值，如果出现粘包的情况，则pos偏移data长度，继续获取data的值
                    self.dump_timestamp.append(timestamp)
                    self.src_ip_list.append(src_ip)
                    self.dst_ip_list.append(dst_ip)
                    self.src_port_list.append(src_port)
                    self.dst_port_list.append(dst_port)
                    temp_str += tempdata[pos:pos + new_order_len]
                    pre_pos = pos     # 记录前一个数据的msgtype的位置
                    pos += new_order_len
                    if len(temp_str) == len(tempdata):   # 当新的字符串的长度等于原tempdata长度则退出
                        flag = False

                elif re_order_cofirm is not None:
                    """委托确认/撤单响应"""
                    self.all_data_list.append(tempdata[pos:pos + order_confirm_len])
                    self.dump_timestamp.append(timestamp)
                    self.src_ip_list.append(src_ip)
                    self.dst_ip_list.append(dst_ip)
                    self.src_port_list.append(src_port)
                    self.dst_port_list.append(dst_port)
                    temp_str += tempdata[pos:pos + order_confirm_len]
                    pre_pos = pos
                    pos += order_confirm_len
                    if len(temp_str) == len(tempdata):
                        flag = False

                elif int_msg_type == 190007:
                    '''撤单请求'''
                    self.all_data_list.append(tempdata[pos:pos + cancel_order_len])
                    self.dump_timestamp.append(timestamp)
                    self.src_ip_list.append(src_ip)
                    self.dst_ip_list.append(dst_ip)
                    self.src_port_list.append(src_port)
                    self.dst_port_list.append(dst_port)
                    temp_str += tempdata[pos:pos + cancel_order_len]
                    pre_pos = pos
                    pos += cancel_order_len
                    if len(temp_str) == len(tempdata):
                        flag = False

                elif int_msg_type == 290008:
                    """撤单失败响应"""
                    self.all_data_list.append(tempdata[pos:pos + cancel_order_failed_len])
                    self.dump_timestamp.append(timestamp)
                    self.src_ip_list.append(src_ip)
                    self.dst_ip_list.append(dst_ip)
                    self.src_port_list.append(src_port)
                    self.dst_port_list.append(dst_port)
                    temp_str += tempdata[pos:pos + cancel_order_failed_len]
                    pre_pos = pos
                    pos += cancel_order_failed_len
                    if len(temp_str) == len(tempdata):
                        flag = False

                elif re_order_match is not None:
                    """委托成交"""
                    self.all_data_list.append(tempdata[pos:pos + match_order_len])
                    self.dump_timestamp.append(timestamp)
                    self.src_ip_list.append(src_ip)
                    self.dst_ip_list.append(dst_ip)
                    self.src_port_list.append(src_port)
                    self.dst_port_list.append(dst_port)
                    temp_str += tempdata[pos:pos + match_order_len]
                    pre_pos = pos
                    pos += match_order_len
                    if len(temp_str) == len(tempdata):
                        flag = False
                else:
                    flag = False

            elif flag_2 == 1:       # 处理不完整的半包情况，如出现一条委托数据不完整，则必将导致后面获取的msgtype的值不对
                slices = pre_pos + 8     # 从上一个msgtype的值往后遍历，直到找到一个对的msgtype的值。当找到后，则将该位置重新赋值给pos
                for n in range(slices, len(tempdata) + 1):
                    tmp_msg_type = int(str(tempdata[n:n + 8]), 16)
                    temp_re = re.match(r'[1,2]\d{3}[0,1][1,2,5,7,8]', str(tmp_msg_type))
                    if temp_re is not None and len(tempdata[n:n + 8]) == 8:
                        pos = n
                        temp_str = tempdata[0:pos]
                        self.all_data_list.pop()   # 删除上一个不完整的数据
                        self.dump_timestamp.pop()
                        self.src_ip_list.pop()
                        self.dst_ip_list.pop()
                        self.src_port_list.pop()
                        self.dst_port_list.pop()
                        break
            else:
                break

    def dump_data_data(self):
        """
        1、根据IP地址和端口号过滤数据
        2、对于长度大于2896的数据包的处理，2896不包括包头的长度（包头长66）
        3、长度大于2896可能出现半包的处理
        4、将每条完整的数据临时存放在sendData和recvData中
        5、cap为是所有数据包组成的一个capture对象，该对象支持迭代
            cap[1033]：表示第1033条数据包
            cap[1033].layers[3]:获取第1033条数据包的第三层
            cap[1033].layers[3].layer_name:获取第1033条数据包的第三层的名称
        6、可使用(dir(cap))获取i里面的方法和属性
        """
        cap = pyshark.FileCapture(self.file_path)
        # print(cap[1033].layers[4])
        # print(dir(cap[1033].layers[3]))
        # print(cap[1033].layers[3])
        # print(hasattr(cap[1033].layers[5], 'data'))
        # print(cap[1033].layers[4].layer_name)
        # print(cap[1033].layers[5].data)
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
                        data = j.data    # 获取DATA层data的属性值

                        # """源IP地址是ORS的IP地址，则为发送数据。如：新订单，撤单请求等"""
                        if i.ip.src_host == self.ors_ip and i.ip.dst_host == self.tgw_ip and i.tcp.srcport == self.ors_port and i.tcp.dstport == self.tgw_port:
                            if sendFlag == 0:
                                if len(data) >= 2896:  # 如果data数据长度（不包含头）超过2896，则会出现半包的情况，需要和下一条数据进行拼接
                                    sendFlag = 1
                                    sendData = sendData + data
                                    continue
                                else:
                                    sendData = data
                                    temp_timestamp = i.sniff_timestamp    # 出现半包时，将半包的时间戳为该笔数据的时间
                                    # 将获取的IP地址、端口号、数据包、时间戳传给data_parse方法进行解析
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

                        # """源IP地址是TGW的IP地址，则为接受数据。如：委托响应，成交响应"""
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

# if __name__ == '__main__':
# dump = Dump_Data('196.168.0.90', '196.168.0.81')
# dump = Dump_Data()
# dump.dump_data_data()

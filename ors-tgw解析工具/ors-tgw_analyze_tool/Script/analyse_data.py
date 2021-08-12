# -*- coding: utf-8 -*-
# @Date : 2021/7/22 11:12
# @File : analyse_data.py
# @Author : Lizi


import csv
import re
import time
from dump_pcap_data import Dump_Data


class Convert:
    all_data_list = []
    all_data = None
    int_msg_type = None
    timestamp = None
    int_partition_no = None
    int_report_index = None
    int_owner_type = None
    int_transact_time = None
    ascii_app_id = None
    ascii_reporting_pbuid = None
    ascii_submitting_pbuid = None
    ascii_security_id = None
    ascii_security_id_source = None
    ascii_clearing_firm = None
    ascii_user_info = None
    ascii_order_id = None
    int_order_qty = None
    int_price = None
    int_ord_rej_reason = None
    ascii_clord_id = None
    ascii_orig_clordid = None
    ascii_exec_id = None
    ascii_exec_type = None
    ascii_ord_status = None
    int_leaves_qty = None
    int_cum_qty = None
    int_last_px = None
    int_last_qty = None
    ascii_side = None
    ascii_ord_type = None
    ascii_account_id = None
    ascii_branch_id = None
    ascii_order_restrictions = None
    ascii_reject_text = None
    int_cxlrej_reason = None

    def __init__(self):
        dump = Dump_Data
        self.orig_data = dump.all_data_list
        self.orig_timestamp = dump.dump_timestamp
        self.orig_src_ip = dump.src_ip_list
        self.orig_dst_ip = dump.dst_ip_list
        self.orig_src_port = dump.src_port_list
        self.orig_dst_port = dump.dst_port_list

    def filter_data(self):
        for data in self.orig_data:
            self.data = data
            # print('data', self.orig_data)
            Msg_Type = self.data[0:8]
            self.int_msg_type = int(str(Msg_Type), 16)  # 十六进制转十进制
            re_new_order = re.match(r'1\d{3}01', str(self.int_msg_type))
            re_order_cofirm = re.match(r'2\d{3}02', str(self.int_msg_type))
            re_order_match = re.match(r'2\d{3}15', str(self.int_msg_type))

            if re_new_order is not None:
                self.msgtype_1xxx01()

            elif re_order_cofirm is not None:
                self.msgtype_2xxx02()

            elif re_order_match is not None:
                self.msgtype_2xxx15()

            elif self.int_msg_type == 190007:
                self.msgtype_190007()

            elif self.int_msg_type == 290008:
                self.msgtype_290008()

    def msgtype_1xxx01(self):
        """新订单"""
        data_index = self.orig_data.index(self.data)
        # self.logger.info(f'MsgType=2XXX02的数据长度为：{len(data)}')
        self.msg_type = self.int_msg_type  # 获取MsgType的值
        # self.logger.info(f'MsgType：{self.msg_type}')

        str_time = self.orig_timestamp[data_index]  # 正则过滤后，根据data数据的索引来获取当前比订单的时间戳
        sec = time.strftime("%Y-%m-%d-%H:%M:%S", time.localtime(int(str_time[0:10])))
        nano = str_time[11:20]
        self.timestamp = f'{sec}{nano}'

        # self.logger.info(f'TimeStamp：{self.timestamp}')

        self.src_ip = self.orig_src_ip[data_index]
        # self.logger.info(f'src_IP：{self.src_ip}')

        self.dst_ip = self.orig_dst_ip[data_index]
        # self.logger.info(f'dst_IP：{self.dst_ip}')

        self.src_port = self.orig_src_port[data_index]
        # self.logger.info(f'src_port：{self.src_port}')

        self.dst_port = self.orig_dst_port[data_index]
        # self.logger.info(f'dst_port：{self.dst_port}')

        App_ID = self.data[16:22]  # 获取App_ID的值
        len_app_id = len(App_ID)
        ascii_app_id_list = []
        for n in range(0, len_app_id, 2):
            int_app_id = int(str(App_ID[n:n + 2]), 16)  # 将十六进制转换成十进制
            ascii_app_id_list.append(chr(int_app_id))  # 将转换后的十进制转换成ascii，添加到ascii_app_id_list列表中
            self.ascii_app_id = ''.join(ascii_app_id_list)  # 将ascii_app_id_list列表转换成字符串
        # self.logger.info(f"App_ID:{self.ascii_app_id}")

        Submitting_PBUID = self.data[22:34]
        len_submitting_pbuid = len(Submitting_PBUID)
        submitting_pbuid_list = []
        for n in range(0, len_submitting_pbuid, 2):
            int_submitting_pbuid = int(str(Submitting_PBUID[n:n + 2]), 16)
            submitting_pbuid_list.append(chr(int_submitting_pbuid))
            self.ascii_submitting_pbuid = ''.join(submitting_pbuid_list)
        # self.logger.info(f"Submitting_PBUID:{self.ascii_submitting_pbuid}")

        Security_ID = self.data[34:50]
        len_security_id = len(Security_ID)
        security_id_list = []
        for n in range(0, len_security_id, 2):
            int_security_id = int(str(Security_ID[n:n + 2]), 16)
            security_id_list.append(chr(int_security_id))
            self.ascii_security_id = ''.join(security_id_list)
        # self.logger.info(f"Security_ID:{self.ascii_security_id}")

        SecurityID_Source = self.data[50:58]
        len_securityid_source = len(SecurityID_Source)
        securityid_source_list = []
        for n in range(0, len_securityid_source, 2):
            int_securityi_source = int(str(SecurityID_Source[n:n + 2]), 16)
            securityid_source_list.append(chr(int_securityi_source))
            self.ascii_security_id_source = ''.join(securityid_source_list)
        # self.logger.info(f"SecurityID_Source:{self.ascii_security_id_source}")

        Owner_Type = self.data[58:62]
        self.int_owner_type = int(str(Owner_Type), 16)
        # self.logger.info(f"Owner_Type:{self.int_owner_type}")

        Clearing_Firm = self.data[62:66]
        len_clearing_firm = len(Clearing_Firm)
        clearing_firm_list = []
        for n in range(0, len_clearing_firm, 2):
            int_clearing_firm = int(str(Clearing_Firm[n:n + 2]), 16)
            clearing_firm_list.append(chr(int_clearing_firm))
            self.ascii_clearing_firm = ''.join(clearing_firm_list)
        # self.logger.info(f"Clearing_Firm:{self.ascii_clearing_firm}")

        Transact_Time = self.data[66:82]
        self.int_transact_time = int(str(Transact_Time), 16)
        # self.logger.info(f"Transact_Time:{self.int_transact_time}")

        User_Info = self.data[82:98]
        len_user_info = len(User_Info)
        user_info_list = []
        for n in range(0, len_user_info, 2):
            int_user_info = int(str(User_Info[n:n + 2]), 16)
            user_info_list.append(chr(int_user_info))
            self.ascii_user_info = ''.join(user_info_list)
        # self.logger.info(f"User_Info:{self.ascii_user_info}")

        ClOrd_ID = self.data[98:118]
        len_clord_id = len(ClOrd_ID)
        clord_id_list = []
        for n in range(0, len_clord_id, 2):
            int_clord_id = int(str(ClOrd_ID[n:n + 2]), 16)
            clord_id_list.append(chr(int_clord_id))
            self.ascii_clord_id = ''.join(clord_id_list)
        # self.logger.info(f"ClOrd_ID:{self.ascii_clord_id}")

        Account_ID = self.data[118:142]
        len_account_id = len(Account_ID)
        account_id_list = []
        for n in range(0, len_account_id, 2):
            int_account_id = int(str(Account_ID[n:n + 2]), 16)
            account_id_list.append(chr(int_account_id))
            self.ascii_account_id = ''.join(account_id_list)
        # self.logger.info(f"Account_ID:{self.ascii_account_id}")

        Branch_ID = self.data[142:150]
        len_branch_id = len(Branch_ID)
        branch_id_list = []
        for n in range(0, len_branch_id, 2):
            int_branch_id = int(str(Branch_ID[n:n + 2]), 16)
            branch_id_list.append(chr(int_branch_id))
            self.ascii_branch_id = ''.join(branch_id_list)
        # self.logger.info(f"Branch_ID:{self.ascii_branch_id}")

        Order_Restrictions = self.data[150:158]
        len_order_restrictions = len(Order_Restrictions)
        order_restrictions_list = []
        for n in range(0, len_order_restrictions, 2):
            int_order_restrictions = int(str(Order_Restrictions[n:n + 2]), 16)
            order_restrictions_list.append(chr(int_order_restrictions))
            self.ascii_order_restrictions = ''.join(order_restrictions_list)
        # self.logger.info(f"Order_Restrictions:{self.ascii_order_restrictions}")

        Side = self.data[158:160]
        len_side = len(Side)
        side_list = []
        for n in range(0, len_side, 2):
            int_side = int(str(Side[n:n + 2]), 16)
            side_list.append(chr(int_side))
            self.ascii_side = ''.join(side_list)
        # self.logger.info(f"Side:{self.ascii_side}")

        Ord_Type = self.data[160:162]
        len_ord_side = len(Ord_Type)
        ord_type_list = []
        for n in range(0, len_ord_side, 2):
            int_ord_type = int(str(Side[n:n + 2]), 16)
            ord_type_list.append(chr(int_ord_type))
            self.ascii_ord_type = ''.join(ord_type_list)
        # self.logger.info(f"Ord_Type:{self.ascii_ord_type}")

        Order_Qty = self.data[162:178]
        self.int_order_qty = int(str(Order_Qty), 16)
        # self.logger.info(f"Order_Qty:{self.int_order_qty}")

        Price = self.data[178:194]
        self.int_price = int(str(Price), 16)
        # self.logger.info(f"Price:{self.int_price}")

        all_data = f'{str(self.timestamp).strip()}', f'{self.src_ip}', f'{self.dst_ip}', f'{self.src_port}', f'{self.dst_port}', f'{str(self.msg_type).strip()}', '', '', \
                   f'{str(self.ascii_app_id).strip()}', '', f'{str(self.ascii_submitting_pbuid).strip()}', \
                   f'{str(self.ascii_security_id).strip()}', f'{str(self.ascii_security_id_source).strip()}', \
                   f'{str(self.int_owner_type).strip()}', f'{str(self.ascii_clearing_firm).strip()}', \
                   f'{str(self.int_transact_time).strip()}', f'{str(self.ascii_user_info).strip()}', '', \
                   f'{str(self.ascii_clord_id)}', '', '', '', '', '', '', '', '', '', f'{str(self.ascii_side).strip()}', \
                   f'{str(self.ascii_ord_type).strip()}', f'{str(self.int_order_qty).strip()}', \
                   f'{str(self.int_price).strip()}', f'{str(self.ascii_account_id).strip()}', \
                   f'{str(self.ascii_branch_id).strip()}', f'{str(self.ascii_order_restrictions).strip()}'
        self.all_data_list.append(all_data)

    def msgtype_2xxx02(self):
        """委托确认"""
        data_index = self.orig_data.index(self.data)
        self.msg_type = self.int_msg_type  # 获取MsgType的值
        # self.logger.info(f'MsgType：{self.msg_type}')

        str_time = self.orig_timestamp[data_index]  # 正则过滤后，根据data数据的索引来获取当前比订单的时间戳
        sec = time.strftime("%Y-%m-%d-%H:%M:%S", time.localtime(int(str_time[0:10])))
        nano = str_time[11:20]
        self.timestamp = f'{sec}{nano}'
        # self.logger.info(f'TimeStamp：{self.timestamp}')

        self.src_ip = self.orig_src_ip[data_index]
        # self.logger.info(f'src_IP：{self.src_ip}')

        self.dst_ip = self.orig_dst_ip[data_index]
        # self.logger.info(f'dst_IP：{self.dst_ip}')

        self.src_port = self.orig_src_port[data_index]
        # self.logger.info(f'src_port：{self.src_port}')

        self.dst_port = self.orig_dst_port[data_index]
        # self.logger.info(f'dst_port：{self.dst_port}')

        Partition_No = self.data[22:24]
        self.int_partition_no = int(str(Partition_No), 16)
        # self.logger.info(f'PartitionNo：{self.int_partition_no}')

        Report_Index = self.data[24:40]  # 获取Report_Index的值
        self.int_report_index = int(str(Report_Index), 16)
        # self.logger.info(f"ReportIndex:{self.int_report_index}")

        App_ID = self.data[40:46]  # 获取App_ID的值
        len_app_id = len(App_ID)
        ascii_app_id_list = []
        for n in range(0, len_app_id, 2):
            int_app_id = int(str(App_ID[n:n + 2]), 16)  # 将十六进制转换成十进制
            ascii_app_id_list.append(chr(int_app_id))  # 将转换后的十进制转换成ascii，添加到ascii_app_id_list列表中
            self.ascii_app_id = ''.join(ascii_app_id_list)  # 将ascii_app_id_list列表转换成字符串
        # self.logger.info(f"App_ID:{self.ascii_app_id}")

        Reporting_PBUID = self.data[46:58]
        len_reporting_pbuid = len(Reporting_PBUID)
        reporting_pbuid_list = []
        for n in range(0, len_reporting_pbuid, 2):
            int_reporting_pbuid = int(str(Reporting_PBUID[n:n + 2]), 16)
            reporting_pbuid_list.append(chr(int_reporting_pbuid))
            self.ascii_reporting_pbuid = ''.join(reporting_pbuid_list)
        # self.logger.info(f"Reporting_PBUID:{self.ascii_reporting_pbuid}")

        Submitting_PBUID = self.data[58:70]
        len_submitting_pbuid = len(Submitting_PBUID)
        submitting_pbuid_list = []
        for n in range(0, len_submitting_pbuid, 2):
            int_submitting_pbuid = int(str(Submitting_PBUID[n:n + 2]), 16)
            submitting_pbuid_list.append(chr(int_submitting_pbuid))
            self.ascii_submitting_pbuid = ''.join(submitting_pbuid_list)
        # self.logger.info(f"Submitting_PBUID:{self.ascii_submitting_pbuid}")

        Security_ID = self.data[70:86]
        len_security_id = len(Security_ID)
        security_id_list = []
        for n in range(0, len_security_id, 2):
            int_security_id = int(str(Security_ID[n:n + 2]), 16)
            security_id_list.append(chr(int_security_id))
            self.ascii_security_id = ''.join(security_id_list)
        # self.logger.info(f"Security_ID:{self.ascii_security_id}")

        SecurityID_Source = self.data[86:94]
        len_securityid_source = len(SecurityID_Source)
        securityid_source_list = []
        for n in range(0, len_securityid_source, 2):
            int_securityi_source = int(str(SecurityID_Source[n:n + 2]), 16)
            securityid_source_list.append(chr(int_securityi_source))
            self.ascii_security_id_source = ''.join(securityid_source_list)
        # self.logger.info(f"SecurityID_Source:{self.ascii_security_id_source}")

        Owner_Type = self.data[94:98]
        self.int_owner_type = int(str(Owner_Type), 16)
        # self.logger.info(f"Owner_Type:{self.int_owner_type}")

        Clearing_Firm = self.data[98:102]
        len_clearing_firm = len(Clearing_Firm)
        clearing_firm_list = []
        for n in range(0, len_clearing_firm, 2):
            int_clearing_firm = int(str(Clearing_Firm[n:n + 2]), 16)
            clearing_firm_list.append(chr(int_clearing_firm))
            self.ascii_clearing_firm = ''.join(clearing_firm_list)
        # self.logger.info(f"Clearing_Firm:{self.ascii_clearing_firm}")

        Transact_Time = self.data[102:118]
        self.int_transact_time = int(str(Transact_Time), 16)
        # self.logger.info(f"Transact_Time:{self.int_transact_time}")

        User_Info = self.data[118:134]
        len_user_info = len(User_Info)
        user_info_list = []
        for n in range(0, len_user_info, 2):
            int_user_info = int(str(User_Info[n:n + 2]), 16)
            user_info_list.append(chr(int_user_info))
            self.ascii_user_info = ''.join(user_info_list)
        # self.logger.info(f"User_Info:{self.ascii_user_info}")

        Order_ID = self.data[134:166]
        len_order_id = len(Order_ID)
        order_id_list = []
        for n in range(0, len_order_id, 2):
            int_order_id = int(str(Order_ID[n:n + 2]), 16)
            order_id_list.append(chr(int_order_id))
            self.ascii_order_id = ''.join(order_id_list)
        # self.logger.info(f"Order_ID:{self.ascii_order_id}")

        ClOrd_ID = self.data[166:186]
        len_clord_id = len(ClOrd_ID)
        clord_id_list = []
        for n in range(0, len_clord_id, 2):
            int_clord_id = int(str(ClOrd_ID[n:n + 2]), 16)
            clord_id_list.append(chr(int_clord_id))
            self.ascii_clord_id = ''.join(clord_id_list)
        # self.logger.info(f"ClOrd_ID:{self.ascii_clord_id}")

        Orig_ClOrdID = self.data[186: 206]
        len_orig_clordid = len(Orig_ClOrdID)
        orig_clordid_list = []
        for n in range(0, len_orig_clordid, 2):
            int_orig_clordid = int(str(Orig_ClOrdID[n:n + 2]), 16)
            orig_clordid_list.append(chr(int_orig_clordid))
            self.ascii_orig_clordid = ''.join(orig_clordid_list)
        # self.logger.info(f"Orig_ClOrdID:{self.ascii_orig_clordid}")

        Exec_ID = self.data[206:238]
        len_exec_id = len(Exec_ID)
        exec_id_list = []
        for n in range(0, len_exec_id, 2):
            int_exec_id = int(str(Exec_ID[n:n + 2]), 16)
            exec_id_list.append(chr(int_exec_id))
            self.ascii_exec_id = ''.join(exec_id_list)
        # self.logger.info(f"Exec_ID:{self.ascii_exec_id}")

        Exec_Type = self.data[238:240]
        len_exec_type = len(Exec_Type)
        exec_type_list = []
        for n in range(0, len_exec_type, 2):
            int_exec_type = int(str(Exec_Type[n:n + 2]), 16)
            exec_type_list.append(chr(int_exec_type))
            self.ascii_exec_type = ''.join(exec_type_list)
        # self.logger.info(f"Exec_Type:{self.ascii_exec_type}")

        Ord_Status = self.data[240:242]
        len_ord_status = len(Ord_Status)
        ord_status_list = []
        for n in range(0, len_ord_status, 2):
            int_ord_status = int(str(Ord_Status[n:n + 2]), 16)
            ord_status_list.append(chr(int_ord_status))
            self.ascii_ord_status = ''.join(ord_status_list)
        # self.logger.info(f"Ord_Status:{self.ascii_ord_status}")

        Ord_Rej_Reason = self.data[242:246]
        self.int_ord_rej_reason = int(str(Ord_Rej_Reason), 16)
        # self.logger.info(f"Ord_Rej_Reason:{self.int_ord_rej_reason}")

        Leaves_Qty = self.data[246:262]
        self.int_leaves_qty = int(str(Leaves_Qty), 16)
        # self.logger.info(f"Leaves_Qty:{self.int_leaves_qty}")

        Cum_Qty = self.data[262:278]
        # print('Cum_Qty:', Cum_Qty, '*****')
        self.int_cum_qty = int(str(Cum_Qty), 16)
        # self.logger.info(f"Cum_Qty:{self.int_cum_qty}")

        Side = self.data[278:280]
        len_side = len(Side)
        side_list = []
        for n in range(0, len_side, 2):
            int_side = int(str(Side[n:n + 2]), 16)
            side_list.append(chr(int_side))
            self.ascii_side = ''.join(side_list)
        # self.logger.info(f"Side:{self.ascii_side}")

        Ord_Type = self.data[280:282]
        len_ord_side = len(Ord_Type)
        ord_type_list = []
        for n in range(0, len_ord_side, 2):
            int_ord_type = int(str(Side[n:n + 2]), 16)
            ord_type_list.append(chr(int_ord_type))
            self.ascii_ord_type = ''.join(ord_type_list)
        # self.logger.info(f"Ord_Type:{self.ascii_ord_type}")

        Order_Qty = self.data[282:298]
        self.int_order_qty = int(str(Order_Qty), 16)
        # self.logger.info(f"Order_Qty:{self.int_order_qty}")

        Price = self.data[298:314]
        self.int_price = int(str(Price), 16)
        # self.logger.info(f"Price:{self.int_price}")

        Account_ID = self.data[314:338]
        len_account_id = len(Account_ID)
        account_id_list = []
        for n in range(0, len_account_id, 2):
            int_account_id = int(str(Account_ID[n:n + 2]), 16)
            account_id_list.append(chr(int_account_id))
            self.ascii_account_id = ''.join(account_id_list)
        # self.logger.info(f"Account_ID:{self.ascii_account_id}")

        Branch_ID = self.data[338:346]
        len_branch_id = len(Branch_ID)
        branch_id_list = []
        for n in range(0, len_branch_id, 2):
            int_branch_id = int(str(Branch_ID[n:n + 2]), 16)
            branch_id_list.append(chr(int_branch_id))
            self.ascii_branch_id = ''.join(branch_id_list)
        # self.logger.info(f"Branch_ID:{self.ascii_branch_id}")

        Order_Restrictions = self.data[346:354]
        len_order_restrictions = len(Order_Restrictions)
        order_restrictions_list = []
        for n in range(0, len_order_restrictions, 2):
            int_order_restrictions = int(str(Order_Restrictions[n:n + 2]), 16)
            order_restrictions_list.append(chr(int_order_restrictions))
            self.ascii_order_restrictions = ''.join(order_restrictions_list)
        # self.logger.info(f"Order_Restrictions:{self.ascii_order_restrictions}")

        # f‘{XXX}’先将每个字符转成一个完整的字符串，最后将所有的字符

        all_data = f'{str(self.timestamp).strip()}', f'{self.src_ip}', f'{self.dst_ip}', f'{self.src_port}', f'{self.dst_port}', f'{str(self.msg_type).strip()}', \
                   f'{str(self.int_partition_no).strip()}', f'{str(self.int_report_index).strip()}', \
                   f'{str(self.ascii_app_id).strip()}', f'{str(self.ascii_reporting_pbuid).strip()}', \
                   f'{str(self.ascii_submitting_pbuid).strip()}', f'{str(self.ascii_security_id).strip()}', \
                   f'{str(self.ascii_security_id_source).strip()}', f'{str(self.int_owner_type).strip()}', \
                   f'{str(self.ascii_clearing_firm).strip()}', f'{str(self.int_transact_time).strip()}', \
                   f'{str(self.ascii_user_info).strip()}', f'{str(self.ascii_order_id).strip()}', \
                   f'{str(self.ascii_clord_id).strip()}', f'{str(self.ascii_orig_clordid).strip()}', \
                   f'{str(self.ascii_exec_id).strip()}', f'{str(self.ascii_exec_type).strip()}', \
                   f'{str(self.ascii_ord_status).strip()}', f'{str(self.int_ord_rej_reason).strip()}', \
                   f'{str(self.int_leaves_qty).strip()}', f'{str(self.int_cum_qty).strip()}', '', '', \
                   f'{str(self.ascii_side).strip()}', f'{str(self.ascii_ord_type).strip()}', \
                   f'{str(self.int_order_qty).strip()}', f'{str(self.int_price).strip()}', \
                   f'{str(self.ascii_account_id).strip()}', f'{str(self.ascii_branch_id).strip()}', \
                   f'{str(self.ascii_order_restrictions).strip()}'
        self.all_data_list.append(all_data)

    def msgtype_2xxx15(self):
        """委托成交"""
        data_index = self.orig_data.index(self.data)
        # self.logger.info(f'MsgType=2XXX15的数据长度为：{len(data)}')
        self.msg_type = self.int_msg_type  # 获取MsgType的值
        # self.logger.info(f'MsgType：{self.msg_type}')

        str_time = self.orig_timestamp[data_index]  # 正则过滤后，根据data数据的索引来获取当前比订单的时间戳
        sec = time.strftime("%Y-%m-%d-%H:%M:%S", time.localtime(int(str_time[0:10])))
        nano = str_time[11:20]
        self.timestamp = f'{sec}{nano}'
        # self.logger.info(f'TimeStamp：{self.timestamp}')

        self.src_ip = self.orig_src_ip[data_index]
        # self.logger.info(f'src_IP：{self.src_ip}')

        self.dst_ip = self.orig_dst_ip[data_index]
        # self.logger.info(f'dst_IP：{self.dst_ip}')

        self.src_port = self.orig_src_port[data_index]
        # self.logger.info(f'src_port：{self.src_port}')

        self.dst_port = self.orig_dst_port[data_index]
        # self.logger.info(f'dst_port：{self.dst_port}')

        Partition_No = self.data[22:24]
        self.int_partition_no = int(str(Partition_No), 16)
        # self.logger.info(f'PartitionNo：{self.int_partition_no}')

        Report_Index = self.data[24:40]  # 获取Report_Index的值
        self.int_report_index = int(str(Report_Index), 16)
        # self.logger.info(f"ReportIndex:{self.int_report_index}")

        App_ID = self.data[40:46]  # 获取App_ID的值
        len_app_id = len(App_ID)
        ascii_app_id_list = []
        for n in range(0, len_app_id, 2):
            int_app_id = int(str(App_ID[n:n + 2]), 16)  # 将十六进制转换成十进制
            ascii_app_id_list.append(chr(int_app_id))  # 将转换后的十进制转换成ascii，添加到ascii_app_id_list列表中
            self.ascii_app_id = ''.join(ascii_app_id_list)  # 将ascii_app_id_list列表转换成字符串
        # self.logger.info(f"App_ID:{self.ascii_app_id}")

        Reporting_PBUID = self.data[46:58]
        len_reporting_pbuid = len(Reporting_PBUID)
        reporting_pbuid_list = []
        for n in range(0, len_reporting_pbuid, 2):
            int_reporting_pbuid = int(str(Reporting_PBUID[n:n + 2]), 16)
            reporting_pbuid_list.append(chr(int_reporting_pbuid))
            self.ascii_reporting_pbuid = ''.join(reporting_pbuid_list)
        # self.logger.info(f"Reporting_PBUID:{self.ascii_reporting_pbuid}")

        Submitting_PBUID = self.data[58:70]
        len_submitting_pbuid = len(Submitting_PBUID)
        submitting_pbuid_list = []
        for n in range(0, len_submitting_pbuid, 2):
            int_submitting_pbuid = int(str(Submitting_PBUID[n:n + 2]), 16)
            submitting_pbuid_list.append(chr(int_submitting_pbuid))
            self.ascii_submitting_pbuid = ''.join(submitting_pbuid_list)
        # self.logger.info(f"Submitting_PBUID:{self.ascii_submitting_pbuid}")

        Security_ID = self.data[70:86]
        len_security_id = len(Security_ID)
        security_id_list = []
        for n in range(0, len_security_id, 2):
            int_security_id = int(str(Security_ID[n:n + 2]), 16)
            security_id_list.append(chr(int_security_id))
            self.ascii_security_id = ''.join(security_id_list)
        # self.logger.info(f"Security_ID:{self.ascii_security_id}")

        SecurityID_Source = self.data[86:94]
        len_securityid_source = len(SecurityID_Source)
        securityid_source_list = []
        for n in range(0, len_securityid_source, 2):
            int_securityi_source = int(str(SecurityID_Source[n:n + 2]), 16)
            securityid_source_list.append(chr(int_securityi_source))
            self.ascii_security_id_source = ''.join(securityid_source_list)
        # self.logger.info(f"SecurityID_Source:{self.ascii_security_id_source}")

        Owner_Type = self.data[94:98]
        self.int_owner_type = int(str(Owner_Type), 16)
        # self.logger.info(f"Owner_Type:{self.int_owner_type}")

        Clearing_Firm = self.data[98:102]
        len_clearing_firm = len(Clearing_Firm)
        clearing_firm_list = []
        for n in range(0, len_clearing_firm, 2):
            int_clearing_firm = int(str(Clearing_Firm[n:n + 2]), 16)
            clearing_firm_list.append(chr(int_clearing_firm))
            self.ascii_clearing_firm = ''.join(clearing_firm_list)
        # self.logger.info(f"Clearing_Firm:{self.ascii_clearing_firm}")

        Transact_Time = self.data[102:118]
        self.int_transact_time = int(str(Transact_Time), 16)
        # self.logger.info(f"Transact_Time:{self.int_transact_time}")

        User_Info = self.data[118:134]
        len_user_info = len(User_Info)
        user_info_list = []
        for n in range(0, len_user_info, 2):
            int_user_info = int(str(User_Info[n:n + 2]), 16)
            user_info_list.append(chr(int_user_info))
            self.ascii_user_info = ''.join(user_info_list)
        # self.logger.info(f"User_Info:{self.ascii_user_info}")

        Order_ID = self.data[134:166]
        len_order_id = len(Order_ID)
        order_id_list = []
        for n in range(0, len_order_id, 2):
            int_order_id = int(str(Order_ID[n:n + 2]), 16)
            order_id_list.append(chr(int_order_id))
            self.ascii_order_id = ''.join(order_id_list)
        # self.logger.info(f"Order_ID:{self.ascii_order_id}")

        ClOrd_ID = self.data[166:186]
        len_clord_id = len(ClOrd_ID)
        clord_id_list = []
        for n in range(0, len_clord_id, 2):
            int_clord_id = int(str(ClOrd_ID[n:n + 2]), 16)
            clord_id_list.append(chr(int_clord_id))
            self.ascii_clord_id = ''.join(clord_id_list)
        # self.logger.info(f"ClOrd_ID:{self.ascii_clord_id}")

        Exec_ID = self.data[186:218]
        len_exec_id = len(Exec_ID)
        exec_id_list = []
        for n in range(0, len_exec_id, 2):
            int_exec_id = int(str(Exec_ID[n:n + 2]), 16)
            exec_id_list.append(chr(int_exec_id))
            self.ascii_exec_id = ''.join(exec_id_list)
        # self.logger.info(f"Exec_ID:{self.ascii_exec_id}")

        Exec_Type = self.data[218:220]
        len_exec_type = len(Exec_Type)
        exec_type_list = []
        for n in range(0, len_exec_type, 2):
            int_exec_type = int(str(Exec_Type[n:n + 2]), 16)
            exec_type_list.append(chr(int_exec_type))
            self.ascii_exec_type = ''.join(exec_type_list)
        # self.logger.info(f"Exec_Type:{self.ascii_exec_type}")

        Ord_Status = self.data[220:222]
        len_ord_status = len(Ord_Status)
        ord_status_list = []
        for n in range(0, len_ord_status, 2):
            int_ord_status = int(str(Ord_Status[n:n + 2]), 16)
            ord_status_list.append(chr(int_ord_status))
            self.ascii_ord_status = ''.join(ord_status_list)
        # self.logger.info(f"Ord_Status:{self.ascii_ord_status}")

        Last_Px = self.data[222:238]
        self.int_last_px = int(str(Last_Px), 16)
        # self.logger.info(f"Last_Px:{self.int_last_px}")

        Last_Qty = self.data[238:254]
        self.int_last_qty = int(str(Last_Qty), 16)
        # self.logger.info(f"Last_Qty:{self.int_last_qty}")

        Leaves_Qty = self.data[254:270]
        self.int_leaves_qty = int(str(Leaves_Qty), 16)
        # self.logger.info(f"Leaves_Qty:{self.int_leaves_qty}")

        Cum_Qty = self.data[270:286]
        self.int_cum_qty = int(str(Cum_Qty), 16)
        # self.logger.info(f"Cum_Qty:{self.int_cum_qty}")

        Side = self.data[286:288]
        len_side = len(Side)
        side_list = []
        for n in range(0, len_side, 2):
            int_side = int(str(Side[n:n + 2]), 16)
            side_list.append(chr(int_side))
            self.ascii_side = ''.join(side_list)
        # self.logger.info(f"Side:{self.ascii_side}")

        Account_ID = self.data[288:312]
        len_account_id = len(Account_ID)
        account_id_list = []
        for n in range(0, len_account_id, 2):
            int_account_id = int(str(Account_ID[n:n + 2]), 16)
            account_id_list.append(chr(int_account_id))
            self.ascii_account_id = ''.join(account_id_list)
        # self.logger.info(f"Account_ID:{self.ascii_account_id}")

        Branch_ID = self.data[312:320]
        len_branch_id = len(Branch_ID)
        branch_id_list = []
        for n in range(0, len_branch_id, 2):
            int_branch_id = int(str(Branch_ID[n:n + 2]), 16)
            branch_id_list.append(chr(int_branch_id))
            self.ascii_branch_id = ''.join(branch_id_list)
        # self.logger.info(f"Branch_ID:{self.ascii_branch_id}")

        all_data = f'{str(self.timestamp).strip()}', f'{self.src_ip}', f'{self.dst_ip}', f'{self.src_port}', f'{self.dst_port}', f'{str(self.msg_type).strip()}', \
                   f'{str(self.int_partition_no).strip()}', f'{str(self.int_report_index).strip()}', \
                   f'{str(self.ascii_app_id).strip()}', f'{str(self.ascii_reporting_pbuid).strip()}', \
                   f'{str(self.ascii_submitting_pbuid).strip()}', f'{str(self.ascii_security_id).strip()}', \
                   f'{str(self.ascii_security_id_source).strip()}', f'{str(self.int_owner_type).strip()}', \
                   f'{str(self.ascii_clearing_firm).strip()}', f'{str(self.int_transact_time).strip()}', \
                   f'{str(self.ascii_user_info).strip()}', f'{str(self.ascii_order_id).strip()}', \
                   f'{str(self.ascii_clord_id).strip()}', '', f'{str(self.ascii_exec_id).strip()}', \
                   f'{str(self.ascii_exec_type).strip()}', f'{str(self.ascii_ord_status).strip()}', '', \
                   f'{str(self.int_leaves_qty).strip()}', f'{str(self.int_cum_qty).strip()}', \
                   f'{str(self.int_last_px)}', f'{str(self.int_last_qty).strip()}', f'{str(self.ascii_side).strip()}', \
                   '', '', '', f'{str(self.ascii_account_id).strip()}', f'{str(self.ascii_branch_id).strip()}', ''
        self.all_data_list.append(all_data)

    def msgtype_190007(self):
        """撤单请求"""
        data_index = self.orig_data.index(self.data)
        # self.logger.info(f'MsgType=2XXX02的数据长度为：{len(data)}')
        self.msg_type = self.int_msg_type  # 获取MsgType的值
        # self.logger.info(f'MsgType：{self.msg_type}')

        str_time = self.orig_timestamp[data_index]  # 正则过滤后，根据data数据的索引来获取当前比订单的时间戳
        sec = time.strftime("%Y-%m-%d-%H:%M:%S", time.localtime(int(str_time[0:10])))
        nano = str_time[11:20]
        self.timestamp = f'{sec}{nano}'
        # self.logger.info(f'TimeStamp：{self.timestamp}')

        self.src_ip = self.orig_src_ip[data_index]
        # self.logger.info(f'src_IP：{self.src_ip}')

        self.dst_ip = self.orig_dst_ip[data_index]
        # self.logger.info(f'dst_IP：{self.dst_ip}')

        self.src_port = self.orig_src_port[data_index]
        # self.logger.info(f'src_port：{self.src_port}')

        self.dst_port = self.orig_dst_port[data_index]
        # self.logger.info(f'dst_port：{self.dst_port}')

        App_ID = self.data[16:22]  # 获取App_ID的值
        len_app_id = len(App_ID)
        ascii_app_id_list = []
        for n in range(0, len_app_id, 2):
            int_app_id = int(str(App_ID[n:n + 2]), 16)  # 将十六进制转换成十进制
            ascii_app_id_list.append(chr(int_app_id))  # 将转换后的十进制转换成ascii，添加到ascii_app_id_list列表中
            self.ascii_app_id = ''.join(ascii_app_id_list)  # 将ascii_app_id_list列表转换成字符串
        # self.logger.info(f"App_ID:{self.ascii_app_id}")

        Submitting_PBUID = self.data[22:34]
        len_submitting_pbuid = len(Submitting_PBUID)
        submitting_pbuid_list = []
        for n in range(0, len_submitting_pbuid, 2):
            int_submitting_pbuid = int(str(Submitting_PBUID[n:n + 2]), 16)
            submitting_pbuid_list.append(chr(int_submitting_pbuid))
            self.ascii_submitting_pbuid = ''.join(submitting_pbuid_list)
        # self.logger.info(f"Submitting_PBUID:{self.ascii_submitting_pbuid}")

        Security_ID = self.data[34:50]
        len_security_id = len(Security_ID)
        security_id_list = []
        for n in range(0, len_security_id, 2):
            int_security_id = int(str(Security_ID[n:n + 2]), 16)
            security_id_list.append(chr(int_security_id))
            self.ascii_security_id = ''.join(security_id_list)
        # self.logger.info(f"Security_ID:{self.ascii_security_id}")

        SecurityID_Source = self.data[50:58]
        len_securityid_source = len(SecurityID_Source)
        securityid_source_list = []
        for n in range(0, len_securityid_source, 2):
            int_securityi_source = int(str(SecurityID_Source[n:n + 2]), 16)
            securityid_source_list.append(chr(int_securityi_source))
            self.ascii_security_id_source = ''.join(securityid_source_list)
        # self.logger.info(f"SecurityID_Source:{self.ascii_security_id_source}")

        Owner_Type = self.data[58:62]
        self.int_owner_type = int(str(Owner_Type), 16)
        # self.logger.info(f"Owner_Type:{self.int_owner_type}")

        Clearing_Firm = self.data[62:66]
        len_clearing_firm = len(Clearing_Firm)
        clearing_firm_list = []
        for n in range(0, len_clearing_firm, 2):
            int_clearing_firm = int(str(Clearing_Firm[n:n + 2]), 16)
            clearing_firm_list.append(chr(int_clearing_firm))
            self.ascii_clearing_firm = ''.join(clearing_firm_list)
        # self.logger.info(f"Clearing_Firm:{self.ascii_clearing_firm}")

        Transact_Time = self.data[66:82]
        self.int_transact_time = int(str(Transact_Time), 16)
        # self.logger.info(f"Transact_Time:{self.int_transact_time}")

        User_Info = self.data[82:98]
        len_user_info = len(User_Info)
        user_info_list = []
        for n in range(0, len_user_info, 2):
            int_user_info = int(str(User_Info[n:n + 2]), 16)
            user_info_list.append(chr(int_user_info))
            self.ascii_user_info = ''.join(user_info_list)
        # self.logger.info(f"User_Info:{self.ascii_user_info}")

        ClOrd_ID = self.data[98:118]
        len_clord_id = len(ClOrd_ID)
        clord_id_list = []
        for n in range(0, len_clord_id, 2):
            int_clord_id = int(str(ClOrd_ID[n:n + 2]), 16)
            clord_id_list.append(chr(int_clord_id))
            self.ascii_clord_id = ''.join(clord_id_list)
        # self.logger.info(f"ClOrd_ID:{self.ascii_clord_id}")

        Orig_ClOrdID = self.data[118:138]
        len_orig_clordid = len(Orig_ClOrdID)
        orig_clordid_list = []
        for n in range(0, len_orig_clordid, 2):
            int_orig_clordid = int(str(Orig_ClOrdID[n:n + 2]), 16)
            orig_clordid_list.append(chr(int_orig_clordid))
            self.ascii_orig_clordid = ''.join(orig_clordid_list)
        # self.logger.info(f"Orig_ClOrdID:{self.ascii_orig_clordid}")

        Side = self.data[138:140]
        len_side = len(Side)
        side_list = []
        for n in range(0, len_side, 2):
            int_side = int(str(Side[n:n + 2]), 16)
            side_list.append(chr(int_side))
            self.ascii_side = ''.join(side_list)
        # self.logger.info(f"Side:{self.ascii_side}")

        Order_ID = self.data[140:172]
        len_order_id = len(Order_ID)
        order_id_list = []
        for n in range(0, len_order_id, 2):
            int_order_id = int(str(Order_ID[n:n + 2]), 16)
            order_id_list.append(chr(int_order_id))
            self.ascii_order_id = ''.join(order_id_list)
        # self.logger.info(f"Order_ID:{self.ascii_order_id}")

        Order_Qty = self.data[172:188]
        self.int_order_qty = int(str(Order_Qty), 16)
        # self.logger.info(f"Order_Qty:{self.int_order_qty}")

        all_data = f'{str(self.timestamp).strip()}', f'{self.src_ip}', f'{self.dst_ip}', f'{self.src_port}', f'{self.dst_port}', f'{str(self.msg_type).strip()}', '', '', \
                   f'{str(self.ascii_app_id).strip()}', '', f'{str(self.ascii_submitting_pbuid).strip()}', \
                   f'{str(self.ascii_security_id).strip()}', f'{str(self.ascii_security_id_source).strip()}', \
                   f'{str(self.int_owner_type).strip()}', f'{str(self.ascii_clearing_firm).strip()}', \
                   f'{str(self.int_transact_time).strip()}', f'{str(self.ascii_user_info).strip()}', \
                   f'{str(self.ascii_order_id).strip()}', f'{str(self.ascii_clord_id).strip()}', \
                   f'{str(self.ascii_orig_clordid).strip()}', '', '', '', '', '', '', '', '', \
                   f'{str(self.ascii_side).strip()}', '', f'{str(self.int_order_qty).strip()}', '', '', '', ''
        self.all_data_list.append(all_data)

    def msgtype_290008(self):
        """"撤单失败"""
        data_index = self.orig_data.index(self.data)
        # self.logger.info(f'MsgType=2XXX02的数据长度为：{len(data)}')
        self.msg_type = self.int_msg_type  # 获取MsgType的值
        # self.logger.info(f'MsgType：{self.int_msg_type}')

        str_time = self.orig_timestamp[data_index]  # 正则过滤后，根据data数据的索引来获取当前比订单的时间戳
        sec = time.strftime("%Y-%m-%d-%H:%M:%S", time.localtime(int(str_time[0:10])))
        nano = str_time[11:20]
        self.timestamp = f'{sec}{nano}'
        # self.logger.info(f'TimeStamp：{self.timestamp}')

        self.src_ip = self.orig_src_ip[data_index]
        # self.logger.info(f'src_IP：{self.src_ip}')

        self.dst_ip = self.orig_dst_ip[data_index]
        # self.logger.info(f'dst_IP：{self.dst_ip}')

        self.src_port = self.orig_src_port[data_index]
        # self.logger.info(f'src_port：{self.src_port}')

        self.dst_port = self.orig_dst_port[data_index]
        # self.logger.info(f'dst_port：{self.dst_port}')

        Partition_No = self.data[22:24]
        self.int_partition_no = int(str(Partition_No), 16)
        # self.logger.info(f'PartitionNo：{self.int_partition_no}')

        Report_Index = self.data[24:40]  # 获取Report_Index的值
        self.int_report_index = int(str(Report_Index), 16)
        # self.logger.info(f"ReportIndex:{self.int_report_index}")

        App_ID = self.data[40:46]  # 获取App_ID的值
        len_app_id = len(App_ID)
        ascii_app_id_list = []
        for n in range(0, len_app_id, 2):
            int_app_id = int(str(App_ID[n:n + 2]), 16)  # 将十六进制转换成十进制
            ascii_app_id_list.append(chr(int_app_id))  # 将转换后的十进制转换成ascii，添加到ascii_app_id_list列表中
            self.ascii_app_id = ''.join(ascii_app_id_list)  # 将ascii_app_id_list列表转换成字符串
        # self.logger.info(f"App_ID:{self.ascii_app_id}")

        Reporting_PBUID = self.data[46:58]
        len_reporting_pbuid = len(Reporting_PBUID)
        reporting_pbuid_list = []
        for n in range(0, len_reporting_pbuid, 2):
            int_reporting_pbuid = int(str(Reporting_PBUID[n:n + 2]), 16)
            reporting_pbuid_list.append(chr(int_reporting_pbuid))
            self.ascii_reporting_pbuid = ''.join(reporting_pbuid_list)
        # self.logger.info(f"Reporting_PBUID:{self.ascii_reporting_pbuid}")

        Submitting_PBUID = self.data[58:70]
        len_submitting_pbuid = len(Submitting_PBUID)
        submitting_pbuid_list = []
        for n in range(0, len_submitting_pbuid, 2):
            int_submitting_pbuid = int(str(Submitting_PBUID[n:n + 2]), 16)
            submitting_pbuid_list.append(chr(int_submitting_pbuid))
            self.ascii_submitting_pbuid = ''.join(submitting_pbuid_list)
        # self.logger.info(f"Submitting_PBUID:{self.ascii_submitting_pbuid}")

        Security_ID = self.data[70:86]
        len_security_id = len(Security_ID)
        security_id_list = []
        for n in range(0, len_security_id, 2):
            int_security_id = int(str(Security_ID[n:n + 2]), 16)
            security_id_list.append(chr(int_security_id))
            self.ascii_security_id = ''.join(security_id_list)
        # self.logger.info(f"Security_ID:{self.ascii_security_id}")

        SecurityID_Source = self.data[86:94]
        len_securityid_source = len(SecurityID_Source)
        securityid_source_list = []
        for n in range(0, len_securityid_source, 2):
            int_securityi_source = int(str(SecurityID_Source[n:n + 2]), 16)
            securityid_source_list.append(chr(int_securityi_source))
            self.ascii_security_id_source = ''.join(securityid_source_list)
        # self.logger.info(f"SecurityID_Source:{self.ascii_security_id_source}")

        Owner_Type = self.data[94:98]
        self.int_owner_type = int(str(Owner_Type), 16)
        # self.logger.info(f"Owner_Type:{self.int_owner_type}")

        Clearing_Firm = self.data[98:102]
        len_clearing_firm = len(Clearing_Firm)
        clearing_firm_list = []
        for n in range(0, len_clearing_firm, 2):
            int_clearing_firm = int(str(Clearing_Firm[n:n + 2]), 16)
            clearing_firm_list.append(chr(int_clearing_firm))
            self.ascii_clearing_firm = ''.join(clearing_firm_list)
        # self.logger.info(f"Clearing_Firm:{self.ascii_clearing_firm}")

        Transact_Time = self.data[102:118]
        self.int_transact_time = int(str(Transact_Time), 16)
        # self.logger.info(f"Transact_Time:{self.int_transact_time}")

        User_Info = self.data[118:134]
        len_user_info = len(User_Info)
        user_info_list = []
        for n in range(0, len_user_info, 2):
            int_user_info = int(str(User_Info[n:n + 2]), 16)
            user_info_list.append(chr(int_user_info))
            self.ascii_user_info = ''.join(user_info_list)
        # self.logger.info(f"User_Info:{self.ascii_user_info}")

        ClOrd_ID = self.data[134:154]
        len_clord_id = len(ClOrd_ID)
        clord_id_list = []
        for n in range(0, len_clord_id, 2):
            int_clord_id = int(str(ClOrd_ID[n:n + 2]), 16)
            clord_id_list.append(chr(int_clord_id))
            self.ascii_clord_id = ''.join(clord_id_list)
        # self.logger.info(f"ClOrd_ID:{self.ascii_clord_id}")

        Orig_ClOrdID = self.data[154:174]
        len_orig_clordid = len(Orig_ClOrdID)
        orig_clordid_list = []
        for n in range(0, len_orig_clordid, 2):
            int_orig_clordid = int(str(Orig_ClOrdID[n:n + 2]), 16)
            orig_clordid_list.append(chr(int_orig_clordid))
            self.ascii_orig_clordid = ''.join(orig_clordid_list)
        # self.logger.info(f"Orig_ClOrdID:{self.ascii_orig_clordid}")

        Side = self.data[174:176]
        len_side = len(Side)
        side_list = []
        for n in range(0, len_side, 2):
            int_side = int(str(Side[n:n + 2]), 16)
            side_list.append(chr(int_side))
            self.ascii_side = ''.join(side_list)
        # self.logger.info(f"Side:{self.ascii_side}")

        Ord_Status = self.data[176:178]
        len_ord_status = len(Ord_Status)
        ord_status_list = []
        for n in range(0, len_ord_status, 2):
            int_ord_status = int(str(Ord_Status[n:n + 2]), 16)
            ord_status_list.append(chr(int_ord_status))
            self.ascii_ord_status = ''.join(ord_status_list)
        # self.logger.info(f"Ord_Status:{self.ascii_ord_status}")

        CxlRej_Reason = self.data[178:182]
        self.int_cxlrej_reason = int(str(CxlRej_Reason), 16)
        # self.logger.info(f"CxlRejReason:{self.int_cxlrej_reason}")

        Reject_Text = self.data[182:214]
        len_reject_text = len(Reject_Text)
        reject_text_list = []
        for n in range(0, len_reject_text, 2):
            int_reject_text = int(str(Reject_Text[n:n + 2]), 16)
            reject_text_list.append(chr(int_reject_text))
            self.ascii_reject_text = ''.join(reject_text_list)
        # self.logger.info(f"Reject_Text:{self.ascii_reject_text}")

        Order_ID = self.data[214:246]
        len_order_id = len(Order_ID)
        order_id_list = []
        for n in range(0, len_order_id, 2):
            int_order_id = int(str(Order_ID[n:n + 2]), 16)
            order_id_list.append(chr(int_order_id))
            self.ascii_order_id = ''.join(order_id_list)
        # self.logger.info(f"Order_ID:{self.ascii_order_id}")

        all_data = f'{str(self.timestamp).strip()}', f'{self.src_ip}', f'{self.dst_ip}', f'{self.src_port}', f'{self.dst_port}', f'{str(self.msg_type).strip()}', \
                   f'{str(self.int_partition_no)}', f'{str(self.int_report_index)}', \
                   f'{str(self.ascii_app_id).strip()}', f'{str(self.ascii_reporting_pbuid)}', \
                   f'{str(self.ascii_submitting_pbuid).strip()}', f'{str(self.ascii_security_id).strip()}', \
                   f'{str(self.ascii_security_id_source).strip()}', f'{str(self.int_owner_type).strip()}', \
                   f'{str(self.ascii_clearing_firm).strip()}', f'{str(self.int_transact_time).strip()}', \
                   f'{str(self.ascii_user_info).strip()}', f'{str(self.ascii_order_id).strip()}', \
                   f'{str(self.ascii_clord_id).strip()}', f'{str(self.ascii_orig_clordid)}', \
                   '', '', f'{str(self.ascii_ord_status)}', '', '', '', '', '', f'{str(self.ascii_side).strip()}', '', \
                   '', '', '', '', '', f'{str(self.int_cxlrej_reason).strip()}', \
                   f'{str(self.ascii_reject_text).strip()}'
        self.all_data_list.append(all_data)


if __name__ == '__main__':
    convert = Convert()
    convert.filter_data()

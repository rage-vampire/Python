# -*- coding: utf-8 -*-
# @Date : 2021/7/29 16:50
# @File : msgtype_2xxx02.py
# @Author : Lizi

import time
from log.log_demo import Log


class MsgType:
    def __init__(self, orig_data, orig_timestamp):
        # self.dump = Dump_Data('196.168.0.90', '196.168.0.81')
        self.orig_data = orig_data
        self.orig_timestamp = orig_timestamp
        self.all_data_list = []
        self.logger = Log('yll', 'console').get_log()
        self.convert = Convert().get_msgtype()
        Convert.get_data()


    def msgtype_2xxx02(self):
        global ascii_app_id, ascii_reporting_pbuid, ascii_submitting_pbuid, ascii_security_id, ascii_security_id_source, \
            ascii_clearing_firm, ascii_user_info, ascii_order_id, ascii_clord_id, ascii_orig_clordid, ascii_exec_id, \
            ascii_exec_type, ascii_ord_status, ascii_side, ascii_ord_type, ascii_account_id, ascii_branch_id, \
            ascii_order_restrictions, int_partition_no, int_report_index, int_owner_type, int_transact_time, \
            int_ord_rej_reason, int_leaves_qty, int_cum_qty, int_order_qty, int_price
        global all_data

        data_index = self.orig_data.index(self.data)
        # self.logger.info(f'MsgType=2XXX02的数据长度为：{len(data)}')
        int_msg_type = self.int_msg_type  # 获取MsgType的值
        self.logger.info(f'MsgType：{int_msg_type}')

        str_time = self.orig_timestamp[data_index]  # 正则过滤后，根据data数据的索引来获取当前比订单的时间戳
        sec = time.strftime("%Y-%m-%d-%H:%M:%S", time.localtime(int(str_time[0:10])))
        nano = str_time[11:20]
        timestamp = f'{sec}{nano}'
        self.logger.info(f'TimeStamp：{timestamp}')

        Partition_No = self.data[22:24]
        int_partition_no = int(str(Partition_No), 16)
        self.logger.info(f'PartitionNo：{int_partition_no}')

        Report_Index = self.data[24:40]  # 获取Report_Index的值
        int_report_index = int(str(Report_Index), 16)
        self.logger.info(f"ReportIndex:{int_report_index}")

        App_ID = self.data[40:46]  # 获取App_ID的值
        len_app_id = len(App_ID)
        ascii_app_id_list = []
        for n in range(0, len_app_id, 2):
            int_app_id = int(str(App_ID[n:n + 2]), 16)  # 将十六进制转换成十进制
            ascii_app_id_list.append(chr(int_app_id))  # 将转换后的十进制转换成ascii，添加到ascii_app_id_list列表中
            ascii_app_id = ''.join(ascii_app_id_list)  # 将ascii_app_id_list列表转换成字符串
        self.logger.info(f"App_ID:{ascii_app_id}")

        Reporting_PBUID = self.data[46:58]
        len_reporting_pbuid = len(Reporting_PBUID)
        reporting_pbuid_list = []
        for n in range(0, len_reporting_pbuid, 2):
            int_reporting_pbuid = int(str(Reporting_PBUID[n:n + 2]), 16)
            reporting_pbuid_list.append(chr(int_reporting_pbuid))
            ascii_reporting_pbuid = ''.join(reporting_pbuid_list)
        self.logger.info(f"Reporting_PBUID:{ascii_reporting_pbuid}")

        Submitting_PBUID = self.data[58:70]
        len_submitting_pbuid = len(Submitting_PBUID)
        submitting_pbuid_list = []
        for n in range(0, len_submitting_pbuid, 2):
            int_submitting_pbuid = int(str(Submitting_PBUID[n:n + 2]), 16)
            submitting_pbuid_list.append(chr(int_submitting_pbuid))
            ascii_submitting_pbuid = ''.join(submitting_pbuid_list)
        self.logger.info(f"Submitting_PBUID:{ascii_submitting_pbuid}")

        Security_ID = self.data[70:86]
        len_security_id = len(Security_ID)
        security_id_list = []
        for n in range(0, len_security_id, 2):
            int_security_id = int(str(Security_ID[n:n + 2]), 16)
            security_id_list.append(chr(int_security_id))
            ascii_security_id = ''.join(security_id_list)
        self.logger.info(f"Security_ID:{ascii_security_id}")

        SecurityID_Source = self.data[86:94]
        len_securityid_source = len(SecurityID_Source)
        securityid_source_list = []
        for n in range(0, len_securityid_source, 2):
            int_securityi_source = int(str(SecurityID_Source[n:n + 2]), 16)
            securityid_source_list.append(chr(int_securityi_source))
            ascii_security_id_source = ''.join(securityid_source_list)
        self.logger.info(f"SecurityID_Source:{ascii_security_id_source}")

        Owner_Type = self.data[94:98]
        int_owner_type = int(str(Owner_Type), 16)
        self.logger.info(f"Owner_Type:{int_owner_type}")

        Clearing_Firm = self.data[98:102]
        len_clearing_firm = len(Clearing_Firm)
        clearing_firm_list = []
        for n in range(0, len_clearing_firm, 2):
            int_clearing_firm = int(str(Clearing_Firm[n:n + 2]), 16)
            clearing_firm_list.append(chr(int_clearing_firm))
            ascii_clearing_firm = ''.join(clearing_firm_list)
        self.logger.info(f"Clearing_Firm:{ascii_clearing_firm}")

        Transact_Time = self.data[102:118]
        int_transact_time = int(str(Transact_Time), 16)
        self.logger.info(f"Transact_Time:{int_transact_time}")

        User_Info = self.data[118:134]
        len_user_info = len(User_Info)
        user_info_list = []
        for n in range(0, len_user_info, 2):
            int_user_info = int(str(User_Info[n:n + 2]), 16)
            user_info_list.append(chr(int_user_info))
            ascii_user_info = ''.join(user_info_list)
        self.logger.info(f"User_Info:{ascii_user_info}")

        Order_ID = self.data[134:166]
        len_order_id = len(Order_ID)
        order_id_list = []
        for n in range(0, len_order_id, 2):
            int_order_id = int(str(Order_ID[n:n + 2]), 16)
            order_id_list.append(chr(int_order_id))
            ascii_order_id = ''.join(order_id_list)
        self.logger.info(f"Order_ID:{ascii_order_id}")

        ClOrd_ID = self.data[166:186]
        len_clord_id = len(ClOrd_ID)
        clord_id_list = []
        for n in range(0, len_clord_id, 2):
            int_clord_id = int(str(ClOrd_ID[n:n + 2]), 16)
            clord_id_list.append(chr(int_clord_id))
            ascii_clord_id = ''.join(clord_id_list)
        self.logger.info(f"ClOrd_ID:{ascii_clord_id}")

        Orig_ClOrdID = self.data[186: 206]
        len_orig_clordid = len(Orig_ClOrdID)
        orig_clordid_list = []
        for n in range(0, len_orig_clordid, 2):
            int_orig_clordid = int(str(Orig_ClOrdID[n:n + 2]), 16)
            orig_clordid_list.append(chr(int_orig_clordid))
            ascii_orig_clordid = ''.join(orig_clordid_list)
        self.logger.info(f"Orig_ClOrdID:{ascii_orig_clordid}")

        Exec_ID = self.data[206:238]
        len_exec_id = len(Exec_ID)
        exec_id_list = []
        for n in range(0, len_exec_id, 2):
            int_exec_id = int(str(Exec_ID[n:n + 2]), 16)
            exec_id_list.append(chr(int_exec_id))
            ascii_exec_id = ''.join(exec_id_list)
        self.logger.info(f"Exec_ID:{ascii_exec_id}")

        Exec_Type = self.data[238:240]
        len_exec_type = len(Exec_Type)
        exec_type_list = []
        for n in range(0, len_exec_type, 2):
            int_exec_type = int(str(Exec_Type[n:n + 2]), 16)
            exec_type_list.append(chr(int_exec_type))
            ascii_exec_type = ''.join(exec_type_list)
        self.logger.info(f"Exec_Type:{ascii_exec_type}")

        Ord_Status = self.data[240:242]
        len_ord_status = len(Ord_Status)
        ord_status_list = []
        for n in range(0, len_ord_status, 2):
            int_ord_status = int(str(Ord_Status[n:n + 2]), 16)
            ord_status_list.append(chr(int_ord_status))
            ascii_ord_status = ''.join(ord_status_list)
        self.logger.info(f"Ord_Status:{ascii_ord_status}")

        Ord_Rej_Reason = self.data[242:246]
        int_ord_rej_reason = int(str(Ord_Rej_Reason))
        self.logger.info(f"Ord_Rej_Reason:{int_ord_rej_reason}")

        Leaves_Qty = self.data[246:262]
        int_leaves_qty = int(str(Leaves_Qty))
        self.logger.info(f"Leaves_Qty:{int_leaves_qty}")

        Cum_Qty = self.data[262:278]
        int_cum_qty = int(str(Cum_Qty))
        self.logger.info(f"Cum_Qty:{int_cum_qty}")

        Side = self.data[278:280]
        len_side = len(Side)
        side_list = []
        for n in range(0, len_side, 2):
            int_side = int(str(Side[n:n + 2]), 16)
            side_list.append(chr(int_side))
            ascii_side = ''.join(side_list)
        self.logger.info(f"Side:{ascii_side}")

        Ord_Type = self.data[280:282]
        len_ord_side = len(Ord_Type)
        ord_type_list = []
        for n in range(0, len_ord_side, 2):
            int_ord_type = int(str(Side[n:n + 2]), 16)
            ord_type_list.append(chr(int_ord_type))
            ascii_ord_type = ''.join(ord_type_list)
        self.logger.info(f"Ord_Type:{ascii_ord_type}")

        Order_Qty = self.data[282:298]
        int_order_qty = int(str(Order_Qty), 16)
        self.logger.info(f"Order_Qty:{int_order_qty}")

        Price = self.data[298:314]
        int_price = int(str(Price), 16)
        self.logger.info(f"Price:{int_price}")

        Account_ID = self.data[314:338]
        len_account_id = len(Account_ID)
        account_id_list = []
        for n in range(0, len_account_id, 2):
            int_account_id = int(str(Account_ID[n:n + 2]), 16)
            account_id_list.append(chr(int_account_id))
            ascii_account_id = ''.join(account_id_list)
        self.logger.info(f"Account_ID:{ascii_account_id}")

        Branch_ID = self.data[338:346]
        len_branch_id = len(Branch_ID)
        branch_id_list = []
        for n in range(0, len_branch_id, 2):
            int_branch_id = int(str(Branch_ID[n:n + 2]), 16)
            branch_id_list.append(chr(int_branch_id))
            ascii_branch_id = ''.join(branch_id_list)
        # self.logger.info(f"Branch_ID:{ascii_branch_id}")

        Order_Restrictions = self.data[346:354]
        len_order_restrictions = len(Order_Restrictions)
        order_restrictions_list = []
        for n in range(0, len_order_restrictions, 2):
            int_order_restrictions = int(str(Order_Restrictions[n:n + 2]), 16)
            order_restrictions_list.append(chr(int_order_restrictions))
            ascii_order_restrictions = ''.join(order_restrictions_list)
        self.logger.info(f"Order_Restrictions:{ascii_order_restrictions}")

        # f‘{XXX}’先将每个字符转成一个完整的字符串，最后将所有的字符
        all_data = f'{timestamp}', f'{str(int_msg_type)}', f'{str(int_partition_no)}', f'{str(int_report_index)}', \
                   f'{str(ascii_app_id)}', f'{str(ascii_reporting_pbuid)}', f'{str(ascii_submitting_pbuid)}', \
                   f'{ascii_security_id}', f'{str(ascii_security_id_source)}', f'{str(int_owner_type)}', \
                   f'{str(ascii_clearing_firm)}', f'{str(int_transact_time)}', f'{str(ascii_user_info)}', \
                   f'{str(ascii_order_id)}', f'{str(ascii_clord_id)}', f'{str(ascii_orig_clordid)}', \
                   f'{str(ascii_exec_id)}', f'{str(ascii_exec_type)}', f'{str(ascii_ord_status)}', \
                   f'{str(int_ord_rej_reason)}', f'{str(int_leaves_qty)}', f'{str(int_cum_qty)}', \
                   f'{str(ascii_side)}', f'{str(ascii_ord_type)}', f'{str(int_order_qty)}', f'{str(int_price)}', \
                   f'{str(ascii_account_id)}', f'{str(ascii_branch_id)}', f'{str(ascii_order_restrictions)}'
        self.all_data_list.append(all_data)

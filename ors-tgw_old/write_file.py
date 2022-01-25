# -*- coding: utf-8 -*-
# @Date : 2021/7/29 17:40
# @File : write_file.py
# @Author : Lizi


import csv
from analyse_data import Convert


# class Write:

def write_csv():
    '''所有订单的表头'''
    all_headers = ['Time_Stamp', 'Msg_Type', 'Partition_No', 'Report_Index', 'App_ID', 'Reporting_PBUID',
                   'Submitting_Pbuid', 'Security_ID', 'Security_ID_Source', 'Owner_Type', 'Clearing_Firm',
                   'Transact_Time', 'User_Info', 'Order_ID', 'Clord_ID', 'Orig_Clord_ID', 'Exec_ID', 'Exec_Type',
                   'Orde_Status', 'OrdRej_Reaseon', 'Leaves_Qty', 'Cum_Qty', 'Last_Px', 'Last_Qty', 'Side', 'Ord_type',
                   'Order_Qty', 'Price', 'Account_ID', 'Branch_ID', 'Order_Restrictions', 'CxlRej_Reason', 'Reject_Text']
    with open('./analyze_data/ors_tgw.csv', mode='w', encoding='utf-8', newline='') as f: # newline去掉空白行
        f_csv = csv.writer(f)  # 写入csv的表头信息
        f_csv.writerow(all_headers)
        for j in range(len(Convert.all_data_list)):
            f_csv.writerow(Convert.all_data_list[j])

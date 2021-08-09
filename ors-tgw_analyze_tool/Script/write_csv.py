# -*- coding: utf-8 -*-
# @Date : 2021/7/29 17:40
# @File : write_csv.py
# @Author : Lizi


import csv
import time
import os

from analyse_data import Convert


# class Write:
def csv_path():
    global file_name
    rp = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
    dir_path = os.path.abspath(os.path.join(os.getcwd(), "../"))     # 获取当前目录的上级目录
    file_path = os.path.join(dir_path, 'Analyze_data/')

    if not os.path.exists(file_path):
        os.mkdir(file_path)
    file_name = file_path + 'ors_tgw_' + rp + '.csv'
    return file_name


def write_csv():
    """所有订单的表头"""
    all_headers = ['Time_Stamp', 'Src_IP', 'Dst_IP', 'Src_Port', 'Dst_Port', 'Msg_Type', 'Partition_No', 'Report_Index',
                   'App_ID', 'Reporting_PBUID',
                   'Submitting_Pbuid', 'Security_ID', 'Security_ID_Source', 'Owner_Type', 'Clearing_Firm',
                   'Transact_Time', 'User_Info', 'Order_ID', 'Clord_ID', 'Orig_Clord_ID', 'Exec_ID', 'Exec_Type',
                   'Orde_Status', 'OrdRej_Reaseon', 'Leaves_Qty', 'Cum_Qty', 'Last_Px', 'Last_Qty', 'Side', 'Ord_type',
                   'Order_Qty', 'Price', 'Account_ID', 'Branch_ID', 'Order_Restrictions', 'CxlRej_Reason',
                   'Reject_Text']
    # with open('../analyze_data/ors_tgw.csv', mode='w', encoding='utf-8', newline='') as f:  # newline去掉空白行
    with open(csv_path(), mode='w', encoding='utf-8', newline='') as f:  # newline去掉空白行
        f_csv = csv.writer(f)  # 写入csv的表头信息
        f_csv.writerow(all_headers)
        for j in range(len(Convert.all_data_list)):
            f_csv.writerow(Convert.all_data_list[j])
    print('-----Write file ending-------')

# if __name__ == '__main__':
#     csv_path()

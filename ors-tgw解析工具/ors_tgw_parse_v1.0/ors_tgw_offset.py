#! pyhon3
# coding=utf-8

import sys
import copy
import csv
import os
import platform
import math


class Order_type:
    O6_timestamp = 0
    O6_string = ""
    O7_timestamp = 0
    O7_string = ""
    account_id = ""
    cli_ord_id = ""
    instrCode = ""
    price = ""
    vol = ""
    msg_type = ""
    market = 102
    side = "-1"

    def __init__(self, O6_timestamp, O6_string, O7_timestamp, O7_string, account_id, cli_ord_id, instrCode, price, vol,
                 msg_type, side):
        self.O6_timestamp = O6_timestamp
        self.O6_string = O6_string
        self.O7_timestamp = O7_timestamp
        self.O7_string = O7_string
        self.account_id = account_id
        self.cli_ord_id = cli_ord_id
        self.instrCode = instrCode
        self.price = price
        self.vol = vol
        self.msg_type = msg_type
        self.market = 102
        self.side = side


def offset_calculate(filePath):
    analyseOutputCsvFile = filePath + "_cap.csv"
    capInfoList = {}

    if os.path.isfile(filePath) == False:
        print("[ERROR]: the file %s does not exist." % filePath)


    csv.field_size_limit(500 * 1024 * 1024)
    with open(filePath, 'r', encoding='utf-8', errors='ignore') as csvfile:
        reader = csv.reader(_.replace('\x00', '') for _ in csvfile)
        for row in reader:
            if len(row) == 0:
                continue
            if row[0].find("Time_Stamp") >= 0:
                continue
            if len(row) >= 16:
                temp_list1 = row[0].split("-")
                temp_list2 = temp_list1[3].split(":")
                temp_list3 = temp_list2[2].split(".")
                pkgstamp = float(temp_list2[0]) * 3600 + float(temp_list2[1]) * 60 + float(temp_list3[0]) + float(
                    temp_list3[1]) / 1000000000
                string_time = row[0]
                if row[5].find("100101") >= 0 or row[5].find("190007") >= 0:
                    if capInfoList.__contains__(row[18]) == False:
                        tempOrderType = Order_type(pkgstamp, string_time, 0, "", row[32], row[18], row[11], row[31],
                                                   row[30], row[5], row[28])
                        capInfoList[row[18]] = tempOrderType
                    else:
                        capInfoList[row[18]].O6_timestamp = pkgstamp
                        capInfoList[row[18]].O6_string = string_time
                        capInfoList[row[18]].account_id = row[32]
                        capInfoList[row[18]].price = row[31]
                elif row[5].find("200102") >= 0:
                    if capInfoList.__contains__(row[18]) == False:
                        tempOrderType = Order_type(0, "", pkgstamp, string_time, row[32], row[18], row[11], row[31],
                                                   row[30], row[5], row[28])
                        capInfoList[row[18]] = tempOrderType
                    else:
                        capInfoList[row[18]].O7_timestamp = pkgstamp
                        capInfoList[row[18]].O7_string = string_time
                        capInfoList[row[18]].account_id = row[32]
                        capInfoList[row[18]].price = row[31]

    with open(analyseOutputCsvFile, 'w') as result_csv:
        result_csv.write(
            "O6p_cap,O7_cap,msg_type,account_id,cli_ord_id,acc_cli,Security_ID,price,vol,market,side,O6pO7_cap")
        for key in capInfoList:
            O6pO7_cap = ""
            if capInfoList.get(key).O7_timestamp != 0 and capInfoList.get(key).O6_timestamp != 0:
                O6pO7_cap = str(int(1000000 * (capInfoList.get(key).O7_timestamp - capInfoList.get(key).O6_timestamp)))
            result_csv.write(
                "\n" + capInfoList.get(key).O6_string.replace(" ", "") + "," + capInfoList.get(key).O7_string.replace(
                    " ", "") + ","
                + capInfoList.get(key).msg_type.replace(" ", "") + "," + capInfoList.get(key).account_id.replace(" ",
                                                                                                                 "") + "," + capInfoList.get(
                    key).cli_ord_id.replace(" ", "")
                + "," + capInfoList.get(key).account_id.replace(" ", "") + "_" + capInfoList.get(
                    key).cli_ord_id.replace(" ", "")
                + "," + capInfoList.get(key).instrCode.replace(" ", "") + "," + capInfoList.get(key).price.replace(" ",
                                                                                                                   "")
                + "," + capInfoList.get(key).vol.replace(" ", "") + ",102," + capInfoList.get(key).side.replace(" ", "")
                + "," + O6pO7_cap)

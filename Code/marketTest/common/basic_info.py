# -*- coding: utf-8 -*-
# !/usr/bin/python
# @Author: WX
# @Create Time: 2020/4/17
# @Software: PyCharm


# 基础参数可参考 https://sc.hkex.com.hk/TuniS/www.hkex.com.hk/Products/Listed-Derivatives/Single%20Stock/Stock-Futures?sc_lang=zh-CN&clienttype=10&clientver=10.2&clientpos=1&clientlang=0&user_id=14573876&web_session_key=hqMklu9Ruqc0m4fNSr8svJVLP9z3B0NU5LWdmoXyJ14e00E5VcmwAzUksiCd4RAbRXXmsWqt7CmesXCwTLn/bMjJ4PrnHPtRZDCv0cNi2P1wdz8vSxNKXAc+inTiKT9+&client_token=81d6aec2a6c63e7634777de86b2e5cde%E4%BA%A4%E6%98%93%E6%89%80%E8%BF%99%E9%87%8C%E6%9C%89%E5%90%88%E7%BA%A6%E8%A7%84%E6%A8%A1

stockFutureInfo = {
    'SHK':{'lotSize': 1000, 'contractMultiplier': 1000},
    'GAH':{'lotSize': 5000, 'contractMultiplier': 5000},
    'FOS': {'lotSize': 10000, 'contractMultiplier': 10000},
    'TWR': {'lotSize': 10000, 'contractMultiplier': 10000},
    'LNK': {'lotSize': 1000, 'contractMultiplier': 1000},
    'SMC': {'lotSize': 5000, 'contractMultiplier': 5000},
    'CTB': {'lotSize': 20000, 'contractMultiplier': 20000},
    'SOA': {'lotSize': 10000, 'contractMultiplier': 10000},
    'ABC': {'lotSize': 10000, 'contractMultiplier': 10000},
    'AIA': {'lotSize': 1000, 'contractMultiplier': 1000},
    'NCL': {'lotSize': 1000, 'contractMultiplier': 1000},
    'CDA': {'lotSize': 5000, 'contractMultiplier': 5000},
    'CRR': {'lotSize': 10000, 'contractMultiplier': 10000},
    'MIU': {'lotSize': 1000, 'contractMultiplier': 1000},
    'CGN': {'lotSize': 10000, 'contractMultiplier': 10000},
    'BUD': {'lotSize': 1000, 'contractMultiplier': 1000},
    'SUN': {'lotSize': 2000, 'contractMultiplier': 2000},
    'MSB': {'lotSize': 10000, 'contractMultiplier': 10000},
    'COG': {'lotSize': 5000, 'contractMultiplier': 5000},
    'AAC': {'lotSize': 1000, 'contractMultiplier': 1000},
    'GAC': {'lotSize': 4000, 'contractMultiplier': 4000},
    'GWM': {'lotSize': 10000, 'contractMultiplier': 10000},
    'SNO': {'lotSize': 1000, 'contractMultiplier': 1000},
    'CPI': {'lotSize': 1000, 'contractMultiplier': 1000},
    'TRF': {'lotSize': 50000, 'contractMultiplier': 50000},
    'CSA': {'lotSize': 5000, 'contractMultiplier': 5000},
    'A50': {'lotSize': 5000, 'contractMultiplier': 5000},
    'HCF': {'lotSize': 5000, 'contractMultiplier': 5000},
    'CHO': {'lotSize': 10000, 'contractMultiplier': 10000},
    'AMC': {'lotSize': 2000, 'contractMultiplier': 2000},
    'EVG': {'lotSize': 2000, 'contractMultiplier': 2000},
    'MET': {'lotSize': 500, 'contractMultiplier': 500},
    'CTS': {'lotSize': 1000, 'contractMultiplier': 1000},
    'HAI': {'lotSize': 10000, 'contractMultiplier': 10000},
    'HTS': {'lotSize': 10000, 'contractMultiplier': 10000},
    'ALB': {'lotSize': 500, 'contractMultiplier': 500},
    'CKH': {'lotSize': 500, 'contractMultiplier': 500},
    'CLP': {'lotSize': 500, 'contractMultiplier': 500},
    'HKG': {'lotSize': 1000, 'contractMultiplier': 1000},
    'WHL': {'lotSize': 1000, 'contractMultiplier': 1000},
    'HKB': {'lotSize': 400, 'contractMultiplier': 400},
    'HEH': {'lotSize': 500, 'contractMultiplier': 500},
    'HSB': {'lotSize': 100, 'contractMultiplier': 100},
    'HLD': {'lotSize': 1000, 'contractMultiplier': 1000},
    'NWD': {'lotSize': 1000, 'contractMultiplier': 1000},
    'SWA': {'lotSize': 500, 'contractMultiplier': 500},
    'BEA': {'lotSize': 200, 'contractMultiplier': 200},
    'GLX': {'lotSize': 1000, 'contractMultiplier': 1000},
    'MTR': {'lotSize': 500, 'contractMultiplier': 500},
    'CIT': {'lotSize': 1000, 'contractMultiplier': 1000},
    'CPA': {'lotSize': 1000, 'contractMultiplier': 1000},
    'CPC': {'lotSize': 2000, 'contractMultiplier': 2000},
    'HEX': {'lotSize': 100, 'contractMultiplier': 100},
    'LIF': {'lotSize': 2000, 'contractMultiplier': 2000},
    'COL': {'lotSize': 2000, 'contractMultiplier': 2000},
    'TCH': {'lotSize': 100, 'contractMultiplier': 100},
    'CTC': {'lotSize': 2000, 'contractMultiplier': 2000},
    'CHU': {'lotSize': 2000, 'contractMultiplier': 2000},
    'PEC': {'lotSize': 2000, 'contractMultiplier': 2000},
    'CNC': {'lotSize': 1000, 'contractMultiplier': 1000},
    'HNP': {'lotSize': 2000, 'contractMultiplier': 2000},
    'ACC': {'lotSize': 500, 'contractMultiplier': 500},
    'CCB': {'lotSize': 1000, 'contractMultiplier': 1000},
    'CHT': {'lotSize': 500, 'contractMultiplier': 500},
    'CSE': {'lotSize': 500, 'contractMultiplier': 500},
    'YZC': {'lotSize': 2000, 'contractMultiplier': 2000},
    'ICB': {'lotSize': 1000, 'contractMultiplier': 1000},
    'CCC': {'lotSize': 1000, 'contractMultiplier': 1000},
    'CCE': {'lotSize': 1000, 'contractMultiplier': 1000},
    'SAN': {'lotSize': 400, 'contractMultiplier': 400},
    'PAI': {'lotSize': 500, 'contractMultiplier': 500},
    'PIC': {'lotSize': 2000, 'contractMultiplier': 2000},
    'BOC': {'lotSize': 500, 'contractMultiplier': 500},
    'ALC': {'lotSize': 2000, 'contractMultiplier': 2000},
    'CLI': {'lotSize': 1000, 'contractMultiplier': 1000},
    'ZJM': {'lotSize': 2000, 'contractMultiplier': 2000},
    'BCM': {'lotSize': 1000, 'contractMultiplier': 1000},
    'KSO': {'lotSize': 1000, 'contractMultiplier': 1000},
    'CMB': {'lotSize': 500, 'contractMultiplier': 500},
    'BCL': {'lotSize': 1000, 'contractMultiplier': 1000}
}



stockIndexFuture = {
    'CHH': {'lotSize': 50, 'contractMultiplier': 50},
    'DHS': {'lotSize': 50, 'contractMultiplier': 50},
    'DHH': {'lotSize': 50, 'contractMultiplier': 50},
    'HHI': {'lotSize': 50, 'contractMultiplier': 50},
    'HSI': {'lotSize': 50, 'contractMultiplier': 50},
    'MBI': {'lotSize': 50, 'contractMultiplier': 50},
    'MCH': {'lotSize': 10, 'contractMultiplier': 10},
    'MHI': {'lotSize': 10, 'contractMultiplier': 10},
    'MOI': {'lotSize': 50, 'contractMultiplier': 50},
    'MPI': {'lotSize': 50, 'contractMultiplier': 50},
    'MXJ': {'lotSize': 100, 'contractMultiplier': 100}
}

rateFuture = {
    'CAU': {'lotSize': 80000, 'contractMultiplier': 80000},
    'CEU': {'lotSize': 50000, 'contractMultiplier': 50000},
    'DHH': {'lotSize': 50, 'contractMultiplier': 50},
    'HHI': {'lotSize': 50, 'contractMultiplier': 50},
    'HSI': {'lotSize': 50, 'contractMultiplier': 50},
    'MBI': {'lotSize': 50, 'contractMultiplier': 50},
    'MCH': {'lotSize': 10, 'contractMultiplier': 10},
    'MHI': {'lotSize': 10, 'contractMultiplier': 10},
    'MOI': {'lotSize': 50, 'contractMultiplier': 50},
    'MPI': {'lotSize': 50, 'contractMultiplier': 50},
    'MXJ': {'lotSize': 100, 'contractMultiplier': 100},
    'CJP': {'lotSize': 60000, 'contractMultiplier': 60000},
    'CUS': {'lotSize': 100000, 'contractMultiplier': 100000},
    'UCN': {'lotSize': 30000, 'contractMultiplier': 30000},

}

pmFuture = {
    'FEM': {'lotSize': 100, 'contractMultiplier': 100},
    'FEQ': {'lotSize': 100, 'contractMultiplier': 100},
    'GDR': {'lotSize': 1000, 'contractMultiplier': 1000},
    'GDU': {'lotSize': 1000, 'contractMultiplier': 1000},
    'LRA': {'lotSize': 5, 'contractMultiplier': 5},
    'LRC': {'lotSize': 5, 'contractMultiplier': 5},
    'LRN': {'lotSize': 1, 'contractMultiplier': 1},
    'LRP': {'lotSize': 5, 'contractMultiplier': 5},
    'LRS': {'lotSize': 1, 'contractMultiplier': 1},
    'LRZ': {'lotSize': 5, 'contractMultiplier': 5}
}


morningStarFuture={'6A':{'contractMultiplier':100000,'lotSize': 100000},
                   '6B':{'contractMultiplier':62500,'lotSize': 62500},
                   '6C':{'contractMultiplier':100000,'lotSize': 100000},
                   '6E':{'contractMultiplier':125000,'lotSize': 125000},
                   '6J':{'contractMultiplier':12500000,'lotSize': 12500000},
                   '6S':{'contractMultiplier':125000,'lotSize': 125000},
                   'QM':{'contractMultiplier':500,'lotSize': 500},
                   'NG':{'contractMultiplier':10000,'lotSize': 10000},
                   'BZ':{'contractMultiplier':1000,'lotSize': 1000},
                   'MYM':{'contractMultiplier':5,'lotSize': 5},#这个字段还在确认中
                   'ZT':{'contractMultiplier':200000,'lotSize': 200000},
                   'ZF':{'contractMultiplier':100000,'lotSize': 100000},
                   'ZN':{'contractMultiplier':100000,'lotSize': 100000},
                   'ZB':{'contractMultiplier':100000,'lotSize': 100000},
                   'ZC':{'contractMultiplier':5000,'lotSize': 5000},
                   'ZS':{'contractMultiplier':5000,'lotSize': 5000},
                   'ZM':{'contractMultiplier':100,'lotSize': 100},
                   'ZW':{'contractMultiplier':5000,'lotSize': 5000},
                   'GC':{'contractMultiplier':100,'lotSize': 100},
                   'SI':{'contractMultiplier':5000,'lotSize': 5000},
                   'HG':{'contractMultiplier':25000,'lotSize': 25000},
                   'QO':{'contractMultiplier':50,'lotSize': 50},
                   'QI':{'contractMultiplier':2500,'lotSize': 2500},
                   'QC':{'contractMultiplier':12500,'lotSize': 12500}}



allFuture = {
    'stockFutureInfo': {'productInfo': stockFutureInfo},
    'stockIndexFuture': {'productInfo': stockIndexFuture},
    'rateFuture': {'productInfo': rateFuture},
    'pmFuture': {'productInfo': pmFuture},
    'morningStarFuture': {'productInfo': morningStarFuture},
}





if __name__ == '__main__':
    print(stockFutureInfo.__len__())
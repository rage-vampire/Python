# -*- coding: utf-8 -*-
# @Date : 2021/7/22 15:23
# @File : dump_pcap_data.py
# @Author : Lizi


from scapy.all import *
import pyshark
from analyse_data import *


# pkts = rdpcap('ors_tgw_bond0_90(1).cap')

class Dump_Data:
    dump_data = []
    dump_timestamp = []

    # def __init__(self, src_ip: str, dst_ip: str):
    #     self.src_ip = src_ip
    #     self.dst_ip = dst_ip

    def data_data_dump(self):
        cap = pyshark.FileCapture('./data_file/all_type_cap.pcap')
        # cap = pyshark.FileCapture('ors_tgw_bond0_90.cap')
        for i in cap:
            # if i.ip.src_host == self.src_ip and i.ip.dst_host == self.dst_ip and 'data' in i:
            if 'data' in i:
                Dump_Data.dump_data.append(i.data.data)
                Dump_Data.dump_timestamp.append(i.sniff_timestamp)
        cap.close()


# if __name__ == '__main__':
# dump = Dump_Data('196.168.0.90', '196.168.0.81')
dump = Dump_Data()
dump.data_data_dump()

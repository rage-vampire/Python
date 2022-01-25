# -*- coding: utf-8 -*-
# @Date : 2021/7/29 17:47
# @File : main.py
# @Author : Lizi
import sys
from write_csv import *
from analyse_data import Convert
from dump_pcap_data import Dump_Data
from ors_tgw_offset import *
from inst_license import *
import getopt


def main():
    src_ip = ''
    dst_ip = ''
    src_port = ''
    dst_port = ''
    filePath = ''
    usage = """
        Usage:
            --help / -h : for help message
            --ors  / -o : ORS_IP:Port
            --tgw  / -t : TGW_IP:Port
            --file / -f : Pcap File Path
            
        Example:
            python ors_tgw_parse.py -f ors_tgw.pcap -o 10.10.10.1:12345  -t 10.10.10.2:8019
            python ors_tgw_parse.py -f ors_tgw.pcap -o 10.10.10.1:12345  -t 10.10.10.2:8019
        """
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hf:o:t:", ["help", "ors=", "tgw=", "file="])
        for opt, value in opts:
            if opt in ("-h", "--help"):
                print(usage)
                sys.exit(1)
            elif opt == "-o":
                orslist=value.split(":")
                src_ip = orslist[0]
                src_port = orslist[1]
            elif opt == "-t":
                tgwlist = value.split(":")
                dst_ip = tgwlist[0]
                dst_port = tgwlist[1]
            elif opt == "-f":
                filePath = value
            else:
                print(usage)
        if len(sys.argv) == 7:
            dump = Dump_Data(src_ip, dst_ip, src_port, dst_port, filePath)
            dump.data_data_dump()
            convert = Convert()
            convert.filter_data()
            write_csv(filePath+".csv")
            offset_calculate(filePath+".csv")
        else:
            print(usage)

    except getopt.GetoptError:
        print(usage)


if __name__ == '__main__':
    check_expiration_day()
    check_used_num()
    main()

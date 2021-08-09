# -*- coding: utf-8 -*-
# @Date : 2021/7/29 17:47
# @File : main.py
# @Author : Lizi
import sys
from write_csv import *
from analyse_data import Convert
from dump_pcap_data import Dump_Data
import getopt


def main():
    global src_ip, dst_ip, src_port, dst_port
    usage = """
        Usage:
            -h: for help message
            --src_ip: The source IP address
            --dst_ip: The destination IP address
            --src_port: The source IP port
            --dst_port: The destination IP port
        Example:
            python main.py --src_ip 196.168.0.81  --dst_ip 196.168.0.91  --src_port 34930  --src_port 8034
        """
    try:
        opts, args = getopt.getopt(sys.argv[1:], "-h", ["help", "src_ip=", "dst_ip=", "src_port=", "dst_port="])
        for opt, value in opts:
            if opt in ("-h", "--help"):
                print(usage)
                sys.exit(1)
            elif opt == "--src_ip":
                src_ip = value
            elif opt == "--dst_ip":
                dst_ip = value
            elif opt == "--src_port":
                src_port = value
            elif opt == "--dst_port":
                dst_port = value
            else:
                print(usage)

    except getopt.GetoptError:
        print(usage)

    if len(sys.argv) == 9:
        # dump = Dump_Data(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
        dump = Dump_Data(src_ip, dst_ip, src_port, dst_port)
        dump.dump_data_data()
        convert = Convert()
        convert.filter_data()
        write_csv()
    else:
        print(usage)


if __name__ == '__main__':
    main()

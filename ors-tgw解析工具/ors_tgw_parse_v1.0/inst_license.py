import os
import platform
import datetime
import sys
import base64
import random
# Usage：
#
# 1. Change EXPIRED_DATE, CAN_USE_TIMES, VERSION value before compile
#
# 2. use in other py file，like below：
#   from license import *
#   if __name__ == '__main__':
#        check_expiration_day()
#        check_used_num()
#        your_function()
#
# 3. if program expired or can not used any more, 
# change EXPIRED_DATE or VERSION ,then compile again, 
# which can reset the environment license
# 

EXPIRED_DATE = "2021-12-31"
CAN_USE_TIMES = "1000"
VERSION = "OTP-v1.0"
PYTHON_VERSION = int(platform.python_version()[0])

def check_expiration_day():
    time_now = datetime.datetime.now()
    expired_time = datetime.datetime.strptime(EXPIRED_DATE, '%Y-%m-%d')

    if expired_time < time_now:
        print("This program has expired.")
        sys.exit()

def encode_or_decode(src, mode):
    if mode == 'encode':
        if PYTHON_VERSION < 3:
            dst = base64.encodestring(src.encode('utf-8'))
        else:
            dst = base64.encodebytes(src.encode('utf-8'))
    elif mode == 'decode':
        if PYTHON_VERSION < 3:
            dst = base64.decodestring(src.encode('utf-8'))
        else:
            dst = base64.decodebytes(src.encode('utf-8'))
    return dst


def check_used_num():
    LICENSE_PATH = ''
    startRandom = ''.join(
        random.choice('zyxwvutsrqponmlkjihgfedc ba!@#$%^&*()=')
        for _ in range(34))
    endRandom = ''.join(
        random.choice('zyxwvutsrqponmlkjihgfedc ba!@#$%^&*()=')
        for _ in range(12))
    if platform.system().lower() == 'linux':
        LICENSE_PATH = os.environ['HOME'] + '/.license.lic'
    elif platform.system().lower() == 'windows':
        if os.path.isdir('D:\\'):
            LICENSE_PATH = 'D:\\license.lic'
        else:
            LICENSE_PATH = '..\license.lic'
    else:
        print("Tools doesn't supported this platform.")
        sys.exit()
    en_date_code = encode_or_decode(EXPIRED_DATE, 'encode')
    en_version_code = encode_or_decode(VERSION, 'encode')
    if os.path.exists(LICENSE_PATH) == False:
        en_code = encode_or_decode(CAN_USE_TIMES, 'encode')
        with open(LICENSE_PATH, 'w+') as file:
            file.write(startRandom + bytes.decode(en_code).replace('\n', '') +
                   bytes.decode(en_date_code).replace('\n', '') + 
                   bytes.decode(en_version_code).replace('\n', '') +endRandom)

    with open(LICENSE_PATH, 'r') as f:
        line = f.readline()

    de_code = encode_or_decode(line[34:42], 'decode')
    date_d_code = line[42:58]
    version_d_code = line[58:70]

    if de_code.isdigit() == False:
        print("This program can not be used any more.")
        sys.exit()
    times = int(de_code)
    if str(en_date_code).find(date_d_code) < 0:
        times = int(CAN_USE_TIMES)
    elif str(en_version_code).find(version_d_code) < 0:
        times = int(CAN_USE_TIMES)
    elif times == 0:
        print("This program can not be used any more")
        sys.exit()
    times = times - 1
    str_times = str(times)
    with open(LICENSE_PATH, 'w') as f:
        if len(str_times) == 3:
            str_times = "0" + str_times
        elif len(str_times) == 2:
            str_times = "00" + str_times
        elif len(str_times) == 1:
            str_times = "000" + str_times
        en_code = encode_or_decode(str_times, 'encode')
        f.write(startRandom + bytes.decode(en_code).replace('\n', '') +
                bytes.decode(en_date_code).replace('\n', '') +
                bytes.decode(en_version_code).replace('\n', '') + endRandom)

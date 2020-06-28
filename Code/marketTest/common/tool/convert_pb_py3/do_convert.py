# -*- coding: utf-8 -*-
# !/usr/bin/python
# @Author: WX
# @Create Time: 2020/4/28
# @Software: PyCharm

import os


def toGetFileName(pathOfSourceProtoFiles, key):
    folderFileList = os.listdir(pathOfSourceProtoFiles)
    fileNameList = []
    for i in folderFileList:
        if key in i:
            fileNameList.append(i)
    return fileNameList


def executeProtoChangeToPy(pathOfSourceProtoFiles, pathToOutput='.\\out\\'):
    protoFileName = toGetFileName(pathOfSourceProtoFiles, ".proto")
    i = 0
    for fileName in protoFileName:
        cmd = os.getcwd() + '\\bin\\protoc.exe --python_out=%s  %s\\%s --proto_path=%s\\' % (pathToOutput, pathOfSourceProtoFiles, fileName, pathOfSourceProtoFiles)
        os.system(cmd)
        i= i + 1
    print('%d pb python files converted!' % i)


if __name__ == '__main__':
    path = os.getcwd() + '\\origin_proto'
    print('Get these proto files converting to python files:', toGetFileName(path, '.proto'))
    executeProtoChangeToPy(path)

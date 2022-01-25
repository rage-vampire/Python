# -*- coding: utf-8 -*-
# @Date : 2021/7/14 16:47
# @File : 02_await.py
# @Author : Lizi

import asyncio


async def hello(index: int):
    print("sleeping....", index)
    await asyncio.sleep(2)
    print("hello world!")


async def entery():
    await hello(1)
    await hello(2)
    await hello(3)


if __name__ == '__main__':
    asyncio.run(entery())







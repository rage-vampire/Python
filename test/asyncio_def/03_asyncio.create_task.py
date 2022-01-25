# -*- coding: utf-8 -*-
# @Date : 2021/7/14 17:06
# @File : 03_asyncio.create_task.py
# @Author : Lizi

import asyncio


async def sum(count: int):
    sum = 0
    print(f"suming.....{count}")
    for step in range(1, count + 1):
        sum += step
        await asyncio.sleep(5)
    print(f"1+....+{count}={sum}")


async def entery():
    tasks = []
    for i in range(10, 15):  # 创建5个Task
        t = asyncio.create_task(sum(i))
        tasks.append(t)

    for n in tasks:
        await n


if __name__ == '__main__':
    asyncio.run(entery())

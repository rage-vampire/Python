# -*- coding: utf-8 -*-
# @Date : 2021/7/6 17:04
# @File : asynico_def.py
# @Author : Lizi

import asyncio


async def coroutine_func(index: int):
    print(f"start a new coroutine,index={index}")
    await asyncio.sleep(1)
    print(f"exit coroutine,index={index}")

if __name__ =="__main__":
    asyncio.run(coroutine_func(1))    # 创建一个事件循环，运行协程 coroutine_func(1) ，最后关闭事件循环
    asyncio.run(coroutine_func(2))    # 创建一个事件循环，运行协程 coroutine_func(2) ，最后关闭事件循环
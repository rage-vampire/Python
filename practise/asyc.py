# -*- coding:utf-8 -*-
# @Filename : asyc.py 
# @Author : Lizi
# @Time : 2020/5/6 20:41 
# @Software: PyCharm


import time
import asyncio

now = lambda: time.time()


async def do_some_work(x):
    print('writing:', x)
    await asyncio.sleep(x)
    return 'Done after {}s'.format(x)


start = now()
coro1 = do_some_work(2)  # 创建一个协程对象coro，这个时候do_some_work函数并没有执行
coro2 = do_some_work(4)
coro3 = do_some_work(5)
print(coro1, coro2, coro3)

loop = asyncio.get_event_loop()  # 创建一个loop事件循环
tasks = [asyncio.ensure_future(coro1),
         asyncio.ensure_future(coro2),
         asyncio.ensure_future(coro3)]  # 创建一个task
print(tasks)

loop.run_until_complete(tasks)  # 将协程添加到事件循环中运行
print('Time:', now() - start)
print('Task ret:', tasks.result())


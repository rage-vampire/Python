# -*- coding:utf-8 -*-
# @Filename : anync.py
# @Author : Lizi
# @Time : 2020/4/10 13:48
# @Software: PyCharm
import asyncio

# 1、
# async def foo():
#     print("这是一个协程")
#
#
# if __name__ == '__main__':
#     loop = asyncio.get_event_loop()
#     try:
#         print("开始运行协程")
#         coro = foo()
#         print("进入事件循环")
#         loop.run_until_complete(coro)
#     finally:
#         print("关闭事件循环")
#         loop.close()

# 2、从协程中返回值
# async def foo():
#     print("这是一个协程")
#     return "返回值"
#
# if __name__ == '__main__':
#     loop = asyncio.get_event_loop()
#     try:
#         print("开始运行协程")
#         coro = foo()
#         print("进入事件循环")
#         result = loop.run_until_complete(coro)
#         print("run_until_complete可以获取协程的{result}，如果没有返回值默认输出None")
#     finally:
#         print("关闭事件循环")
#         loop.close()


# 3、协程调用协程
# async def result1():
#     print("这是result1协程")
#     return "result1"
#
#
# async def result2(arg):
#     print("这是result2协程")
#     return f"result2接收了一个参数,{arg}"
#
#
# async def main():
#     print("主协程")
#     print("等待result1协程运行")
#     res1 = await result1()
#     print("等待result2协程运行")
#     res2 = await result2(res1)
#     return (res1, res2)
#
#
# if __name__ == '__main__':
#     loop = asyncio.get_event_loop()
#     try:
#         result = loop.run_until_complete(main())
#         print(f"获取返回值:{result}")
#     finally:
#         print("关闭事件循环")
#         loop.close()

# 协程中调用普通函数
# call_soon

# import functools

# def callback(args, kwargs="defalut"):
#     print("普通函数做为回调函数,获取参数:{},{}".format(args, kwargs))
#
#
# async def main():
#     print("注册callback")
#     loop.call_soon(callback,1)
#     wrapped = functools.partial(callback, kwargs="not defalut")
#     loop.call_soon(wrapped,2)
#     await asyncio.sleep(0.2)
#
#
# if __name__ == '__main__':
#     loop = asyncio.get_event_loop()
#     try:
#         loop.run_until_complete(main())
#     finally:
#         loop.close()



# 5、call_later
import asyncio


def callback(n):
    print("callback {} invoked".format(n))


async def main(loop):
    print("注册callbacks")
    loop.call_later(3, callback, 1)
    loop.call_later(4, callback, 2)
    loop.call_soon(callback, 3)
    await asyncio.sleep(delay=5)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main(loop))
    finally:
        loop.close()

# 5、
# def foo(future, result):
#     print(f"此时future的状态1:{future}")
#     print(f"设置future的结果:{result}")
#     future.set_result(result)
#     print(f"此时future的状态2:{future}")
#
#
# if __name__ == '__main__':
#     loop = asyncio.get_event_loop()
#     try:
#         all_done = asyncio.Future()
#         loop.call_soon(foo, all_done, "Future is done!")
#         print("进入事件循环")
#         result = loop.run_until_complete(all_done)
#         print("返回结果", result)
#     finally:
#         print("关闭事件循环")
#         loop.close()
#         print("获取future的结果", all_done.result())

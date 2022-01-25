# -*- coding: utf-8 -*-
# @Date : 2021/12/19 15:31
# @File : cir_test.py
# @Author : Lizi


"""
    一个球从300米的高空落下，每次落下弹起3/4的高度，当高度小于0.0001时，球为静止状态。
    求：
    1、求静止时一共弹起多少次
    2、求静止时，一共走过多少距离（即弹起---落下的路程）
"""


def test(h):
    flag = True
    count = 0    # 记录弹起的次数
    dis = 0      # 记录经过的路程
    while flag:
        if h > 0.0001:
            count += 1     # 当高度大于0.0001时，则会落下一次，count+1，
            dis += h       # 每次落下dis都会增加下落时h的高度
            h = (3 * h) / 4
            # upper_h = h     # 弹起的高度
            dis += h  # 每次弹起dis也会增加弹起后的高度
        else:
            flag = False
    return count, dis


if __name__ == '__main__':
    result = test(300)
    print('球静止一共弹起{}次，一共走过{}距离'.format(result[0], result[1]))

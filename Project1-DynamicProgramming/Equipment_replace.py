# -*- coding:utf-8 -*-
"""
作者：Jiazhi He
日期：2021年12月21日
"""


from main import *


def equip_replace_state_choice(state, stage):
    stage_next = stage + 1
    state_pos = [1]
    if state < 5:
        state_pos.append(state + 1)
    return [stage_next, state_pos]


def equip_replace_recur_equa(init_stage, init_state, next_state):
    s = [None, 50, 25, 10, 5, 2]
    c = [30, 40, 50, 75, 90]
    new_cost = [100, 105, 110, 115, 120]
    if next_state == 1:
        return -new_cost[init_stage-1] + s[init_state] - c[0]
    else:
        # print(init_state)
        return -c[init_state]


def final_ret(init_stage, init_state):
    return 0


replace_eq = Dynamicprogramming(equip_replace_recur_equa, equip_replace_state_choice, 6, final_ret)
print(replace_eq(1, 2)[0])
print(replace_eq(1, 2)[1])

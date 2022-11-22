# -*- coding:utf-8 -*-
"""
作者：Jiazhi He
日期：2021年12月20日
"""


from main import *
weight_group = [3, 4, 5]
value_group = [4, 5, 6]


def knapsack_alternatives(state, stage):
    stage_next = stage + 1
    state_pos = [state]
    while state_pos[-1] - weight_group[stage] >= 0:
        state_pos.append(state_pos[-1] - weight_group[stage])
    return [stage_next, state_pos]


def knapsack_recurequa(init_stage, init_state, next_state):
    return value_group[init_stage] * int((init_state - next_state) / weight_group[init_stage])


def final_ret(init_stage, init_state):
    return value_group[init_stage - 1] * int(init_state / weight_group[init_stage - 1])


bag_fill = Dynamicprogramming(knapsack_recurequa, knapsack_alternatives, 3, final_ret)   # stage_final == 3
print(bag_fill(0, 10)[0])   # 10 is the backpack capacity
print(bag_fill(0, 10)[1])

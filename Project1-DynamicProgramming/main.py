# -*- coding:utf-8 -*-
"""
作者：Jiazhi He
日期：2021年12月18日
"""


class Dynamicprogramming:
    def __init__(self, recur_equa, state_choice, stage_final, final_ret):
        """
        recur_equa: a function takes current_stage, current_state, next_stage, next-state as input
        """
        self.recur_equa = recur_equa
        self.state_choice = state_choice
        self.stage_final = stage_final
        self.final_ret = final_ret

    def __call__(self, init_stage, init_state):
        if init_stage == self.stage_final:
            return ['stage:' + str(init_stage) + ';state:' + str(init_state) + '\n', self.final_ret(init_stage, init_state)]
        next_stage, state_list = self.state_choice(init_state, init_stage)
        max_ret = float('-inf')
        state_str = 'stage:' + str(init_stage) + ';state:' + str(init_state) + '\n'
        for next_state in state_list:
            out = self(next_stage, next_state)
            ret = self.recur_equa(init_stage, init_state, next_state) + out[1]
            if ret > max_ret:
                max_ret = ret
                dec_paths = state_str + out[0]
        return [dec_paths, max_ret]

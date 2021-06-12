from random import randint
# import time, math
# import numpy as np
# from copy import deepcopy
from typing import List



def random_ai(board: List[List[int]], current: int, newest: List[int], reversal: List[List[int]], prompt) -> List[int]:
    '''
    这里存放 AI 的算法.
    我这里只保留了一个随机 AI.
    每个 AI 都是一个函数, 并且只能是一个函数!

    输入, 即参数为:
    board: 二维数组, 8 x 8 的棋盘数据, 0 代表空, 1 代表黑棋, 2 代表白棋.
    current: 当前你的棋子颜色, 1 代表黑棋, 2 代表白棋.
    最重要的就是上面两个, 其他输入无关紧要.
    newest: 对方下的最后一个棋子位置.
    reversal: 对方上一次翻转的棋子.
    prompt: 当前你可以下的位置, 即提示. 一般来说你并不需要它.

    返回:
    返回你要下的位置, 例如 [2, 1] 或 (2, 1), 要注意是从 0 开始的.
    '''
    return prompt['list'][randint(0, len(prompt['list']) - 1)]



from random import randint

def random_ai(board: list[list[int]], current: int, newest: list[int], reversal: list[list[int]], prompt) -> list[int]:
    return prompt['list'][randint(0, len(prompt['list']) - 1)]
    
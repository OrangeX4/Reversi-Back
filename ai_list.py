from random import randint
import numpy as np
from copy import deepcopy


def random_ai(board: list[list[int]], current: int, newest: list[int], reversal: list[list[int]], prompt) -> list[int]:
    return prompt['list'][randint(0, len(prompt['list']) - 1)]


def jie_giegie(board: list[list[int]], current: int, newest: list[int], reversal: list[list[int]], prompt) -> list[int]:
    # 杰哥
    class Piece():
        def __init__(self):
            self.available = []
            self.empty = True
            self.black = True

        def is_empty(self):
            if self.empty == True:
                return True
            else:
                return False

        def is_black(self):
            if self.empty == False and self.black == True:
                return True
            else:
                return False

        def is_white(self):
            if self.empty == False and self.black == False:
                return True
            else:
                return False

        def is_available(self):
            if len(self.available) != 0:
                return True
            else:
                return False

    set = np.array([[100, -30, 20, 10, 10, 20, -30, 100],
                    [-30, -60,  1,  -3, -3, 1, -60,  -40],
                    [20,  1, 7, 5, 5,  7,  1,  20],
                    [10,  -3, 5, 5, 5,  5,  -3,  10],
                    [10,  -3, 5, 5,  5, 5, -3,  10],
                    [20,  1,  7,  5, 5, 7,  1,  20],
                    [-30, -60, 1, -3,  -3,  1, -60,  -30],
                    [100,  -30, 20, 10, 10, 20, -30, 100]])

    class Chessboard():
        last_board = []

        def __init__(self):
            self.board = [[Piece() for i in range(0, 8)] for i in range(0, 8)]
            self.board[3][3].empty = False
            self.board[3][3].black = False
            self.board[3][4].empty = False
            self.board[3][4].black = True
            self.board[4][3].empty = False
            self.board[4][3].black = True
            self.board[4][4].empty = False
            self.board[4][4].black = False
            self.last_board = self.board.copy()

        def reverse(self, position, black_turn):
            for direc in self.board[position[0]-1][position[1]-1].available:
                for posi in direc:
                    self.board[posi[0]][posi[1]].black = black_turn

        def set_piece(self, piece: Piece, position: tuple) -> bool:
            if self.board[position[0]-1][position[1]-1].empty == True and self.board[position[0]-1][position[1]-1].available:
                self.last_board = self.board.copy()
                self.reverse(position, piece.black)
                self.board[position[0]-1][position[1]-1] = piece
                return True
            else:
                return False

        def set_black_piece(self, position: tuple) -> bool:
            p1 = Piece()
            p1.empty = False
            p1.black = True
            return self.set_piece(p1, position)

        def set_white_piece(self, position: tuple) -> bool:
            p2 = Piece()
            p2.empty = False
            p2.black = False
            return self.set_piece(p2, position)

        def set_empty_piece(self, position: tuple):
            p3 = Piece()
            self.board[position[0]-1][position[1]-1] = p3

        def get_piece(self, position: tuple) -> Piece:
            return self.board[position[0]-1][position[1]-1]

        def isEmpty(self, position: tuple) -> bool:
            if self.board[position[0]-1][position[1]-1].empty == True:
                return True
            else:
                return False

        def regret(self):
            self.board = self.last_board.copy()

        def available_place(self, black_turn):
            def get_place(row, col, black_turn, direction):
                if 0 <= row+direction[0] <= 7 and 0 <= col+direction[1] <= 7 and \
                    self.board[row + direction[0]][col + direction[1]].black != black_turn and\
                        self.board[row + direction[0]][col + direction[1]].empty == False:
                    ls = []
                    while 0 <= row+direction[0] < 8 and 0 <= col + direction[1] < 8:
                        if self.board[row+direction[0]][col + direction[1]].empty == True:
                            break
                        elif self.board[row+direction[0]][col + direction[1]].black == black_turn:
                            ls.append((row, col))
                            return ls
                        else:
                            ls.append((row, col))
                            row += direction[0]
                            col += direction[1]

            for i in range(0, 8):
                for j in range(0, 8):
                    if self.board[i][j].empty == True:
                        self.board[i][j].available = []
                        for direction in [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]:
                            if get_place(i, j, black_turn, direction) != None:
                                self.board[i][j].available.append(
                                    get_place(i, j, black_turn, direction))

    class robot():
        def __init__(self, figure_set):
            self.analyse_times = 3
            self.figure_set = figure_set
            '分析次数'

        def analyse(self, board: Chessboard, black_turn: bool):
            board.available_place(black_turn)
            reverse_max = -100000
            better_position = []
            for i in range(0, 8):
                for j in range(0, 8):
                    if board.board[i][j].available:
                        count = self.figure_set[i][j]
                        for p in board.board[i][j].available:
                            for posi in p:
                                count += 2 * self.figure_set[posi[0]][posi[1]]
                        if count > reverse_max:
                            reverse_max = count
                            better_position = (i, j)
            return better_position, reverse_max

        def deep_analyse(self, times, board: Chessboard, black_turn: bool):
            if times == 0:
                board.available_place(black_turn)
                return self.analyse(board, black_turn)
            else:
                best_points = -100000
                best_position = (-1, -1)
                board.available_place(black_turn)
                for i in range(0, 8):
                    for j in range(0, 8):
                        if board.board[i][j].available:
                            board_new = deepcopy(board)
                            if black_turn:
                                board_new.set_black_piece((i+1, j+1))
                            else:
                                board_new.set_white_piece((i+1, j+1))
                            new_position, figure = self.deep_analyse(
                                times-1, board_new, not black_turn)
                            count = self.figure_set[i][j]
                            for p in board.board[i][j].available:
                                for posi in p:
                                    count += self.figure_set[posi[0]][posi[1]]
                            if count - figure > best_points:
                                best_points = self.figure_set[i][j] - figure
                                best_position = (i, j)
                return best_position, best_points

        def out_put(self, board: Chessboard, black_turn: bool):
            better_place, figure = self.deep_analyse(
                self.analyse_times, board, black_turn)
            return (better_place[0]+1, better_place[1]+1)
    
    # ---------------------------------------------------------------
    #                          开始适配                              |
    # --------------------------------------------------------------- 

    chessboard = Chessboard()
    for i in range(0, 8):
        for j in range(0, 8):
            if board[i][j] == 0:
                chessboard.board[i][j] = Piece()
            elif board[i][j] == 1:
                new_piece = Piece()
                new_piece.empty = False
                new_piece.black = True
                chessboard.board[i][j] = new_piece
            elif board[i][j] == 2:
                new_piece = Piece()
                new_piece.empty = False
                new_piece.black = False
                chessboard.board[i][j] = new_piece

    ai = robot(set)
    out = ai.out_put(chessboard, current == 1)
    return [out[0] - 1, out[1] - 1]


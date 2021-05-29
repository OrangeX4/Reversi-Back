from random import randint
import numpy as np
from copy import deepcopy


# ⑨
def random_ai(board: list[list[int]], current: int, newest: list[int], reversal: list[list[int]], prompt) -> list[int]:
    return prompt['list'][randint(0, len(prompt['list']) - 1)]


# 杰哥
jie_set = np.array([[100, -30, 20, 10, 10, 20, -30, 100],
                [-30, -60,  1,  -3, -3, 1, -60,  -40],
                [20,  1, 7, 5, 5,  7,  1,  20],
                [10,  -3, 5, 5, 5,  5,  -3,  10],
                [10,  -3, 5, 5,  5, 5, -3,  10],
                [20,  1,  7,  5, 5, 7,  1,  20],
                [-30, -60, 1, -3,  -3,  1, -60,  -30],
                [100,  -30, 20, 10, 10, 20, -30, 100]])


def jie_giegie(board: list[list[int]], current: int, newest: list[int], reversal: list[list[int]], prompt) -> list[int]:
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
        def __init__(self,figure_set):
            self.analyse_times = 3
            self.figure_set = figure_set
            '分析次数'
        
        @staticmethod
        def Change_figure_set(figure_set,position):
            if position[0] == 0:
                figure_set[1][position[1]] = 40
                if position[1] == 0:
                    figure_set[1][1] = 60
                    figure_set[0][1] = 40
                else:
                    figure_set[0][6] = 40
                    figure_set[1][6] = 60
            else:
                figure_set[6][position[1]] = 40
                if position[1] == 0:
                    figure_set[6][1] = 60
                    figure_set[7][1] = 40
                else:
                    figure_set[7][6] = 40
                    figure_set[6][6] = 60

        def analyse(self,board:Chessboard,black_turn:bool):
            board.available_place(black_turn)
            reverse_max = -100000
            better_position = []
            for i in range(0,8):
                for j in range(0,8):
                    if board.board[i][j].available:
                        count = self.figure_set[i][j]
                        if i % 7 == 0 and j % 7 == 0:
                            new_figure_set = self.figure_set.copy()
                            self.Change_figure_set(new_figure_set,(i,j))
                            for p in board.board[i][j].available:
                                for posi in p:
                                    count += 2 * new_figure_set[posi[0]][posi[1]]
                        else:
                            for p in board.board[i][j].available:
                                for posi in p:
                                    count += 2 * self.figure_set[posi[0]][posi[1]]
                        if count > reverse_max:
                            reverse_max = count
                            better_position = (i,j)
            return better_position , reverse_max

        def deep_analyse(self,times,board:Chessboard,black_turn:bool):
            board.available_place(black_turn)
            count = 0
            for i in range(0,8):
                for j in range(0,8):
                    if board.board[i][j].available:
                        count += 1 
            if times == 0:
                board.available_place(black_turn)
                return self.analyse(board,black_turn)
            
            elif count == 0:
                return (0,0),0
            
            else:
                best_points = -100000
                best_position = (-1,-1)
                for i in range(0,8):
                    for j in range(0,8):
                        if board.board[i][j].available:
                            board_new = deepcopy(board)
                            if black_turn:
                                board_new.set_black_piece((i+1,j+1))
                            else:
                                board_new.set_white_piece((i+1,j+1))
                            new_position, figure = self.deep_analyse(times-1,board_new,not black_turn)
                            count = self.figure_set[i][j]
                            for p in board.board[i][j].available:
                                for posi in p:
                                    count += self.figure_set[posi[0]][posi[1]]
                            if count - figure > best_points:
                                best_points = self.figure_set[i][j] - figure
                                best_position = (i,j)
                return best_position,best_points
            

        def out_put(self, board:Chessboard,black_turn:bool):
            better_place,figure = self.deep_analyse(self.analyse_times,board,black_turn)
            return (better_place[0]+1,better_place[1]+1)

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

    ai = robot(jie_set)
    out = ai.out_put(chessboard, current == 1)
    # 在四个角落下棋的话, 需要更改 set
    if (out[0]-1) % 7 == 0 and (out[1]-1) % 7 == 0:
        ai.Change_figure_set(jie_set, (out[0]-1, out[1]-1))
    return [out[0] - 1, out[1] - 1]



# -------------------------------------------------------
# czz
# -------------------------------------------------------
def czz(board: list[list[int]], current: int, newest: list[int], reversal: list[list[int]], prompt) -> list[int]:
    class Board:
        def __init__(self, board: list[list[int]], config: dict=None, history: bool=True, displayer=None) -> None:
            # player init
            self.empty = 0
            self.black = 1
            self.white = 2
            self.avail = 3 # a status won't be stored
            self.name = {self.white: 'white', self.black: 'black', self.empty: 'empty', self.avail: 'avail'}
            # game init
            self.board = np.array(board)
            self.player = self.black
            self.action = {}
            self.history = None
            if history:
                self.history = []

            # gui
            self.displayer = None
            if displayer:
                self.displayer = displayer
                self.displayer.init(self)
            # empty opening
            self._no_avail = 0
            self._record()
            self.end()
            # for next stage
            self.next_stage()

        def _record(self, add_piece: str=None):
            # Pay attention to mutable objects
            if isinstance(self.history, list):
                self.history.append(dict(
                    player=self.player, 
                    action=self.action.copy(), 
                    add_piece=add_piece,
                    board=self.board.copy()))

        def _position_generator(self, start_p: tuple, direction: tuple) -> list:
            x, y = start_p
            dx, dy = direction
            board = self.board
            r = []
            r.append(((x, y), board[x][y]))
            status = True
            while(status):
                try:
                    x, y = x+dx, y+dy
                    if x < 0 or y < 0:
                        raise Exception
                    temp = board[x][y]
                    r.append(((x, y), temp))
                except Exception:
                    status = False
            return r
        
        def _available_action(self, line: list, player: int) -> list:
            '''Return a list contains origin_actions
            line: a list of 2-tuples containing positions and piece
            '''
            pieces = ''.join((map(lambda item: str(item[1]), line)))
            pattern = r'12+0' if player == 1 else r'21+0'
            r = []
            import re
            search_r = re.search(pattern, pieces)
            while(search_r):
                # append position
                start = search_r.span()[0]
                end = search_r.span()[1]-1
                # action is a dict containing 'action': tuple and 'reversi': list of tuples
                action = line[end][0]
                reversi = [ line[i][0] for i in range(start+1, end)]
                r.append(dict(action=action, reversi=reversi))
                # slice for two sequences
                pieces = pieces[search_r.span()[1]:]
                line = line[search_r.span()[1]:]
                # re-search
                search_r = re.search(pattern, pieces)
            return r
        
        def end(self, silent=False):
            '''
            Decide who wins and modify the current pieces rate.
            if some wins, return True and the player_id. player_id is None when it is a tie
            else return False and None
            '''
            self.rate = {self.black: 0, self.white: 0}
            rate = self.rate
            board = self.board
            for x in range(8):
                for y in range(8):
                    if board[x][y] != self.empty:
                        rate[board[x][y]] += 1
            
            if (rate[self.black] + rate[self.white] == 64) or self._no_avail == 2:
                if rate[self.black] == rate[self.white]:
                    if self.displayer and silent==False:
                        self.displayer.display()
                        self.displayer.display(mode='info', message=['Both you win and both you lose.'])
                    return True, None
                else:
                    winner = self.black if rate[self.black] > rate[self.white] else self.white
                    if self.displayer and silent==False:
                        self.displayer.display()
                        self.displayer.display(mode='info', message=['Winner is {}'.format(self.name[winner]), '比分：黑{}:{}白'.format(self.rate[self.black], self.rate[self.white])])
                    return True, winner
            else:
                return False, None
        
        def switch(self, displayer, history):
            '''
            For displayer, give a object(None is OK)
            For history, False for off, True for on
            '''
            self.displayer = displayer
            if not history:
                self.history = None
                

        def next_stage(self):
            player = self.player
            origin_action = []
            board = self.board
            # for xie
            for i in range(15):
                x, y = (0 if i <= 7 else i - 7, 7-i if i <=7 else 0) #03
                origin_action.extend(self._available_action(self._position_generator((x, y), (1, 1)), player))
            for i in range(15):
                x, y = (i if i <= 7 else 7, 7 if i <=7 else 14-i) #30
                origin_action.extend(self._available_action(self._position_generator((x, y), (-1, -1)), player))
            for i in range(15):
                x, y = (0 if i <= 7 else i - 7, i if i <=7 else 7) #12
                origin_action.extend(self._available_action(self._position_generator((x, y), (1, -1)), player))
            for i in range(15):
                x, y = (i if i <= 7 else 7, 0 if i <=7 else i-7) #21
                origin_action.extend(self._available_action(self._position_generator((x, y), (-1, 1)), player))

            # for zheng
            for i in range(8):
                origin_action.extend(self._available_action([((i, j), board[(i, j)]) for j in range(8)], player))
            for i in range(8):
                origin_action.extend(self._available_action([((i, j), board[(i, j)]) for j in reversed(range(8))], player))
            for i in range(8):
                origin_action.extend(self._available_action([((j, i), board[(j, i)]) for j in range(8)], player))
            for i in range(8):
                origin_action.extend(self._available_action([((j, i), board[(j, i)]) for j in reversed(range(8))], player))

            # make a decision about next player
            if len(origin_action) == 0:
                if self.displayer:
                    self.displayer.display(mode='info', message=['现在是{}'.format(self.displayer.piece[self.player]), '当前比分：黑{}:{}白'.format(self.rate[self.black], self.rate[self.white])])
                    self.displayer.display()
                    # change player
                    player = 1 if player == 2 else 2
                    self.displayer.display(mode='info', message=[r'No available action, pass to', self.name[player]])
                else:
                    player = 1 if player == 2 else 2
                # take effect
                self.player = player
                # no available action record
                self._no_avail += 1
                self._record()
                # update rate
                self.end(silent=True)
                return self.player
            else:
                # wash actions
                # str_position: set of reversi positions
                d_action = {}
                for d in origin_action:
                    action = d['action']
                    action = str(action)
                    reversi = d['reversi']
                    if d_action.get(action):
                        d_action[action].update(reversi)
                    else:
                        d_action[action] = set(reversi)
                self.action = d_action
                self._no_avail = 0
                if self.displayer:
                    self.displayer.display(mode='info', message=['现在是{}'.format(self.displayer.piece[self.player]), '当前比分：黑{}:{}白'.format(self.rate[self.black], self.rate[self.white])])
                    self.displayer.display()
                return self.player

        def do_action(self, str_action: str=None):
            # Input
            if not str_action:
                str_action = '({}, {})'.format(*(input().split()))
                # to do: kill list
                while(str_action not in self.action.keys()):
                    if self.displayer:
                        self.displayer.display(mode='info', message=['Invalid action'])
                    str_action = '({}, {})'.format(*(input().split()))
            if len(self.action.keys()) == 0:
                return
            # fetch data
            player = self.player
            board = self.board
            reversi = self.action[str_action]
            # reversi
            for position in reversi:
                x, y = position
                board[x][y] = player
            # put piece
            x, y = eval(str_action)
            board[x][y] = player
            self._record(add_piece=str_action)
            # empty action for correct display of pass-situation
            self.action = {}
            
            # for next stage change player
            self.player = 1 if player == 2 else 2
            self.next_stage()


    def rollout_policy(board):
        '''
        Return a list contain action and their random prob
        '''
        # randomly rollout
        probs = np.random.rand(len(board.action.keys()))
        return list(zip(board.action.keys(), probs))

    def average_policy(board):
        '''
        Return a list contain action and an average prob
        '''
        probs = np.ones(len(board.action.keys()))/len(board.action.keys())
        return list(zip(board.action.keys(), probs))

    class TreeNode(object):
        """A node in the MCTS tree. Each node keeps track of its own value Q,
        prior probability P, and its visit-count-adjusted prior score u.
        """

        def __init__(self, parent, prob) -> None:
            self._parent = parent
            self._children = {} # a map from action to TreeNode
            self._n_visits = 0
            self._Q = 0
            self._u = 0
            self._P = prob

        def expand(self, action_probs):
            """
            Expand tree by creating new children.
            action_priors: a list of tuples of actions and their probability
            """
            if len(action_probs) == 0:
                self._children['no_avail'] = TreeNode(self, 1.0)
            else:
                for action, prob in action_probs:
                    if action not in self._children.keys():
                        self._children[action] = TreeNode(self, prob)
        
        def select(self, c_puct):
            return max(self._children.items(),
                    key=lambda act_node: act_node[1].get_value(c_puct))
        
        def update(self, leaf_value):
            '''
            leaf_value is 1, -1 or 0
            '''
            # Count visit.
            self._n_visits += 1
            # Update Q, a running average of values for all visits.
            self._Q += 1.0*(leaf_value - self._Q) / self._n_visits
        
        def update_recursive(self, leaf_value):
            """Like a call to update(), but applied recursively for all ancestors.
            """
            # If it is not root, this node's parent should be updated first.
            if self._parent:
                self._parent.update_recursive(-leaf_value)
            self.update(leaf_value)

        def get_value(self, c_puct):

            self._u = (c_puct * self._P *
                    np.sqrt(self._parent._n_visits) / (1 + self._n_visits))
            return self._Q + self._u

        def is_leaf(self):
            """Check if leaf node (i.e. no nodes below this have been expanded).
            """
            return self._children == {}

        def is_root(self):
            return self._parent is None

    class MCTS(object):
        def __init__(self, policy_value_fn, c_puct=5, n_playout=10000):
            self._root = TreeNode(None, 1.0)
            self._policy = policy_value_fn
            self._c_puct = c_puct
            self._n_playout = n_playout
        
        def _playout(self, copied_board):
            copied_board.switch(None, False)
            node = self._root
            while(True):
                if node.is_leaf():
                    break
                action, node = node.select(self._c_puct)
                copied_board.do_action(action)

            # here we get a leaf
            action_probs = self._policy(copied_board)
            end, winner = copied_board.end(silent=True)
            if not end:
                node.expand(action_probs)

            # begin rollout
            leaf_value = self._rollout(copied_board)

            node.update_recursive(-leaf_value)

        def _rollout(self, board, limit=500):
            """Use the rollout policy to play until the end of the game,
            returning +1 if the current player wins, -1 if the opponent wins,
            and 0 if it is a tie.
            """
            player = board.player
            for i in range(limit):
                end, winner = board.end()
                if end:
                    if winner == player:
                        return 1
                    elif winner == None:
                        return 0
                    else:
                        return -1
                action_probs = rollout_policy(board)
                if len(action_probs) == 0:
                    action_probs = [('no_avail', 1.0), ]
                max_action, _ = max(action_probs, key=lambda action_prob: action_prob[1])

                board.do_action(max_action)
            else:
                #print("WARNING: rollout reached move limit")
                return 0
        
        def get_move(self, board):
            for i in range(self._n_playout):
                copied_board = deepcopy(board)
                self._playout(copied_board)

            return sorted(self._root._children.items(),
                            key=lambda act_node: act_node[1]._n_visits)[-1]


    class MCTSPlayer(object):
        def __init__(self, c_puct=5, n_playout=50):
            self.mcts = MCTS(average_policy, c_puct, n_playout)

        def do_action(self, board):
            move = self.mcts.get_move(board)
            print(move[0])
            board.do_action(move[0])
        
        def get_action(self, board):
            move = self.mcts.get_move(board)
            return eval(move[0])

    mcts_ai = MCTSPlayer()
    ai_board = Board(board)
    ai_board.player = current
    # ai_board.player = 2 if current == 1 else 1
    ai_board.next_stage()
    return mcts_ai.get_action(ai_board)
            
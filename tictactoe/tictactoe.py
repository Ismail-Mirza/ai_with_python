"""
Tic Tac Toe Player
"""

import math
import copy
X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    x_count = 0
    O_count = 0
    for states in board:
        for state in states:
            if state == X:
                x_count += 1
            elif state == O:
                O_count += 1
    if x_count > O_count:
        return O
    else :
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    result = set()
    i = 0;
    while  i <len(board):
        j = 0 ;
        while  j < len(board):
            if board[i][j] == EMPTY:
                result.add((i,j))
            j += 1
        i += 1
    return result

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    #calcaluting which turn of the given board
    turn  = player(board)
    new_board = copy.deepcopy(board)
    if new_board[action[0]][action[1]] == EMPTY:
        new_board[action[0]][action[1]] = turn
        return new_board
    else:
         Exception("Actions Must be valid")



def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    #looking horizontal winner
    i = 0
    while i < len(board):
        j  = 1
        while j <len(board):
            if board[i][j-1]==board[i][j] and board[i][j] == board[i][j+1]:
                return board[i][j]
            j += 2
        i += 1
    #looking vertical winner
    i = 1
    while i < len(board):
        j  = 0
        while j <len(board):
            if board[i-1][j]==board[i][j] and board[i][j] == board[i+1][j]:
                return board[i][j]
            j += 1
        i += 2
    #looking diagonal winner
    if board[1][1] ==board[0][0] and board[1][1] == board[2][2]:
        return board[1][1]

    elif board[1][1] ==board[0][2] and board[1][1] == board[2][0]:
        return board[1][1]
    else:
        return None






def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) or len(actions(board)) == 0:
        return True
    return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board)==O:
        return -1
    else :
        return 0


# #def minimax(board):
#     """
#     Returns the optimal action for the current player on the board.
#     """
#     if terminal(board):
#         return None
#     min_actions1 = actions(board)
#     #min player
#     root_tr=[]
#     root_max=[]
#     root_min=[]
#     for min_action1 in min_actions1:
#         min_board1 = result(board,min_action1)
#         max_actions1 = actions(min_board1)
#         #max player
#         max1_tr = []
#         max1_max = []
#         max1_min= []
#         for max_action1 in max_actions1:
#             max_board1 = result(min_board1,max_action1)
#             min_actions2 = actions(max_board1)
#             #min player
#             min2_tr = []
#             min2_max=[]
#             min2_min =[]
#             for min_action2 in min_actions2:
#                 min_board2 = result(max_board1,min_action2)
#                 max_actions2 = actions(min_board2)
#                 #max2 player
#                 max2_tr = []
#                 max2_max =[]
#                 max2_min = []
#                 for max_action2 in max_actions2:
#                     max_board2 = result(min_board2,max_action2)
#                     last_actions = actions(max_board2)
#                     #min player
#                     min_out_last = []
#                     max_out_last = []
#                     tr_out_last = []
#                     for last_action in last_actions:
#                         last_board = result(max_board2,last_action)
#                         last_util = utility(last_board)
#                         if last_util < 0:
#                             min_out_last.append(last_action)
#                         elif last_util > 0 :
#                             max_out_last.append(last_action)
#                         else:
#                             tr_out_last.append(last_action)
#                     if len(max_out_last) > 0:
#                         max2_max.append(max_action2)
#                     elif len(tr_out_last)>0 :
#                         max2_tr .append(max_action2)
#                     else:
#                         max2_min.append(max_actions2)
#                 if len(max2_min) > 0:
#                     min2_min.append(min_action2)
#                 elif len(max2_tr)>0:
#                     min2_tr.append(min_actions2)
#                 else:
#                     min2_max.append(min_action2)
#             #max player 1 pick min player 2 max value
#             if len(min2_max) > 0:
#                 max1_max.append(max_action1)
#             elif len(min2_tr) > 0:
#                 max1_tr.append(max_action1)
#             else:
#                 max1_min.append(max_action1)
#         #min player 1 pick min value of max player 1
#         max1_tr.reverse()
#         max1_max.reverse()
#         max1_min.reverse()
#         if len(max1_min)>0:
#             root_min.append(min_action1)
#         elif len(max1_tr)>0:
#             root_tr.append(min_action1)
#         else:
#             root_max.append(min_action1)
#     #return final action
#     if len(root_min) > 0:
#         print(f"play for win actions by ai {root_min}")
#         return root_min[0]
#     elif len(root_tr) > 0 and len(root_min)==0:
#         middle = [(0,1),(1,1),(1,0),(1,2),(2,1)]
#         for action in root_tr:
#             if action in middle:
#                 return action
#         print(f"play for tie by ai {root_tr}")
#         return root_tr[0]
#     else :
#         print(f"root max actions by ai {root_max}")
#         return root_max[0]
def minimax(board):
    if terminal(board):
        return None
    play = player(board)
    if play == "O" : #min player
        actions_player = actions(board)
        min_action = {}
        for action in actions_player:
            min_action[action]=max_value(result(board,action))
        min_u= min(min_action.values())
        for key,val in min_action.items():
            if val == min_u:
                return key
    else: #max player
        actions_player = actions(board)
        max_action = {}
        for action in actions_player:
            max_action[action]=min_value(result(board,action))
        max_u = max(max_action.values())
        for key,val in max_action.items():
            if val == max_u:
                return key

def max_value(board):
    if terminal(board):
        return utility(board)
    v = -10
    for action in actions(board):
        v=max(v,min_value(result(board,action)))
    return v
def min_value(board):
    if terminal(board):
        return utility(board)
    v = 10
    for action in actions(board):
        v= min(v,max_value(result(board,action)))
    return v

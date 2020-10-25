from tictactoe import player,actions,winner,minimax
EMPTY = None
X="X"
O="O"
import copy
# print(actions([[X, EMPTY, EMPTY],
#         [EMPTY, X, O],
#         [EMPTY,O, EMPTY]]))
board = [[X, O, EMPTY],
        [X, EMPTY, EMPTY],
        [EMPTY,O, EMPTY]]
new_board = copy.deepcopy(board)
new_board[0][0] = "hellow"
print(minimax(board))

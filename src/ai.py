import random
import time
import math
import copy
from generator import *
from heuristic import *

node = 0
transposition_table = {}

class tree:

    def __init__(self, board):
        self.board = board
        self.visits = 0
        self.score = 0
        self.children = []

class hawkins:

    def search(self, mx, player, last_move, castling_chance):
        global transposition_table
        global node
        white_pieces = {"P", "R", "K", "Q", "N", "B"}
        black_pieces = {"p", "r", "k", "q", "n", "b"}
        root = tree(mx)

        black_castling = [True if x != 0 else False for x in castling_chance][2:]
        plays = []
        matrices = generator.possible_matrix(mx, player, black_pieces, last_move, black_castling)[0] #all possible plays
        quiet = False
        for matrix in matrices:
            child_node = tree(matrix)
            plays.append(child_node)
        for child in plays:
            root.children.append(child) #create child_nodes in case they havent been created yet
        cicles = 1
        starting_point = time.time()
        for depth in range(1, 4):
            if depth == 3:
                quiet = True
            for child in root.children:
                child.score = hawkins.minimax(self, child.board, depth, -1*10**6, 1*10**6, False, castling_chance, last_move, quiet)
            cicles += 1
            root.children = sorted(root.children, key = lambda child: child.score, reverse = True)
            best_move = hawkins.best_child(self, root).board
            if time.time() - starting_point >= 10:
                transposition_table = {}
                print(node)
                print(cicles)
                node = 0
                return best_move
            else:
                transposition_table = {}
                continue
        print(node)
        node = 0
        print(cicles)
        return best_move

    def q_search(self, mx, depth, alpha, beta, maximizing_player, castling_chance, last_move):
        global transposition_table
        global node
        white_pieces = {"P", "R", "K", "Q", "N", "B"}
        black_pieces = {"p", "r", "k", "q", "n", "b"}
        node += 1
        if depth == 0:
            transposition_table[mx] = points.evaluate(mx)
            return transposition_table[mx]

        eval = points.evaluate(mx)
        if eval >= beta:
            return beta
        alpha = max(alpha, eval)


        if not maximizing_player: player, pieces = "White", white_pieces
        else: player, pieces = "Black", black_pieces
        capture_moves = generator.possible_matrix(mx, player, pieces, last_move, [False, False])[2]
        for capture in capture_moves:
            node += 1
            eval = -hawkins.q_search(self, capture, depth-1, -alpha, -beta, not maximizing_player, castling_chance, last_move) #negamax hybrid
            if eval >= beta:
                return beta
            alpha = max(alpha, eval)
        transposition_table[mx] = alpha    
        return alpha

    def minimax(self, mx, depth, alpha, beta, maximizing_player, castling_chance, last_move, quiet):
        global node
        global transposition_table
        white_pieces = {"P", "R", "K", "Q", "N", "B"}
        black_pieces = {"p", "r", "k", "q", "n", "b"}
        black_castling = [True if x != 0 else False for x in castling_chance][2:]
        white_castling = [True if x != 0 else False for x in castling_chance][:2]
        node += 1
        if depth == 0:
            if quiet:
               return hawkins.q_search(self, mx, 2, alpha, beta, maximizing_player, castling_chance, last_move)
            if mx in transposition_table.keys():
                return transposition_table[mx]
            transposition_table[mx] = points.evaluate(mx)
            return transposition_table[mx]

        if not maximizing_player:
            if True in white_castling:
                if mx[7*8+4] != "K":
                    white_castling = [False, False]
                else:
                    if white_castling[0] == True and mx[7*8] != "R":
                        white_castling[0] = False
                    if white_castling[1] == True and mx[7*8 + 7]!= "R":
                        white_castling[1] = False
            player, pieces, updated_castling = "White", white_pieces, white_castling
        else:
            if True in black_castling:
                if mx[4] != "k":
                    black_castling = [False, False]
                else:
                    if black_castling[0] == True and mx[0] != "r":
                        black_castling[0] = False
                    if black_castling[1] == True and mx[7]!= "r":
                        black_castling[1] = False            
            player, pieces, updated_castling = "Black", black_pieces, black_castling
        moves_generator = generator.possible_matrix(mx, player, pieces, last_move, updated_castling) 
        possible_states = moves_generator[0]


        if len(possible_states) == 0:
            if rules.is_attacked(mx, player, pieces, last_move, False):
                if player == "White":
                    transposition_table[mx] = 300
                    return 300
                else:
                    transposition_table[mx] = -300
                    return -300
            transposition_table[mx] = 0
            return 0

        if maximizing_player:
            max_eval = -1*10**6
            for state in possible_states:
                node+= 1
                #print(state)
                if state in transposition_table.keys():
                    eval = transposition_table[state]
                else:
                    eval = hawkins.minimax(self, state, depth-1, alpha, beta, False, castling_chance, last_move, quiet)
                    transposition_table[state] = eval
                if eval > max_eval:
                    max_eval = eval
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = 1*10**6
            for state in possible_states:
                node += 1
                if state in transposition_table.keys():
                    eval = transposition_table[state]
                else:
                    eval = hawkins.minimax(self, state, depth-1, alpha, beta, True, castling_chance, last_move, quiet)
                    transposition_table[state] = eval
                if eval < min_eval:
                    min_eval = eval
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    def best_child(self,root):
        threshold = -1*10**6
        #print("we_got_here")
        for child in root.children:
            #print(points.evaluate(child.board))
            if child.score > threshold:
                win_choice = child
                threshold = child.score
        #print("hey", points.evaluate(win_choice.board))
        return win_choice


generator = generator()
points = points()
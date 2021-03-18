import random
import time
import math
import copy
from generator import *
from heuristic import *

node = 0
cut = 0
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
        global cut
        
        quiet = False

        root = tree(mx)

        starting_point = time.time()
        for depth in range(1, 6):
            #print(depth)
            best_move = hawkins.minimax(self, root.board, depth, -1*10**5, 1*10**5, True, castling_chance, last_move, quiet)[1]
            if time.time() - starting_point >= 10:
                transposition_table = {}
                #print(node)
                #print(cut)
                cut = 0
                node = 0
                return best_move
            else:
                print(node)
                transposition_table = {}
                transposition_table[root.board] = best_move
                continue
        print(node)
        node = 0
        return best_move

    def q_search(self, mx, depth, alpha, beta, maximizing_player, castling_chance, last_move):
        global transposition_table
        global node
        global cut
        white_pieces = {"P", "R", "K", "Q", "N", "B"}
        black_pieces = {"p", "r", "k", "q", "n", "b"}
        node += 1
        evaluation = points.evaluate(mx)
        if depth == 0:
            return (evaluation, mx)
        if evaluation >= beta:
            cut += 1
            return (beta, mx)
        alpha = max(alpha, evaluation)

        if not maximizing_player: player, pieces = "White", white_pieces
        else: player, pieces = "Black", black_pieces

        capture_moves = generator.possible_matrix(mx, player, pieces, last_move, [False, False])[2]
        for capture in capture_moves:
            node += 1
            eval = hawkins.q_search(self, capture, depth-1, -beta, -alpha, not maximizing_player, castling_chance, last_move) #negamax hybrid
            if -eval[0] >= beta:
                cut += 1
                return (beta, mx)
            alpha = max(alpha, -eval[0])   
        return (alpha, mx)

    def minimax(self, mx, depth, alpha, beta, maximizing_player, castling_chance, last_move, quiet):
        global node
        global cut
        global transposition_table

        white_pieces = {"P", "R", "K", "Q", "N", "B"}
        black_pieces = {"p", "r", "k", "q", "n", "b"}
        black_castling = [True if x != 0 else False for x in castling_chance][2:]
        white_castling = [True if x != 0 else False for x in castling_chance][:2]
        node += 1
        if depth == 0:
            if quiet:
               return hawkins.q_search(self, mx, 2, alpha, beta, not maximizing_player, castling_chance, last_move)
            return (points.evaluate(mx), mx)

        if not maximizing_player:
            if True in white_castling:
                #print(mx)
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
        if mx in transposition_table.keys():
            print("insertion")
            possible_states.insert(0, transposition_table[mx])

        if len(possible_states) == 0:
            if rules.is_attacked(mx, player, pieces, last_move, False):
                if player == "White":
                    return (10000, mx)
                else:
                    return (-10000, mx)
            transposition_table[mx] = 0
            return (0, mx)

        if mx in transposition_table.keys():
            possible_states.insert(0, transposition_table[mx])
        
        if maximizing_player:
            max_eval = -1*10**5
            for state in possible_states:
                node+= 1
                #print(state)
                if state in transposition_table.keys():
                    eval = (points.evaluate(transposition_table[state]), transposition_table[state])
                else:
                    eval = hawkins.minimax(self, state, depth-1, alpha, beta, False, castling_chance, last_move, quiet)
                    transposition_table[state] = eval[1]
                #if depth == 5:
                    #print(eval[0], state)
                if eval[0] > max_eval:
                    max_eval = eval[0]
                    chosen = state
                alpha = max(alpha, eval[0])
                if beta <= alpha:
                    cut += 1
                    break
            return (max_eval, chosen)

        else:
            min_eval = 1*10**5
            for state in possible_states:
                node += 1
                if state in transposition_table.keys():
                    eval = (points.evaluate(transposition_table[state]), transposition_table[state])
                else:
                    eval = hawkins.minimax(self, state, depth-1, alpha, beta, True, castling_chance, last_move, quiet)
                    transposition_table[state] = eval[1]
                if eval[0] < min_eval:
                    min_eval = eval[0]
                    chosen = state
                beta = min(beta, eval[0])
                if beta <= alpha:
                    cut += 1
                    break
            return (min_eval, chosen)


generator = generator()
points = points()
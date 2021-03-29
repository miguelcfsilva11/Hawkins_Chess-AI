import random
import time
import math
import copy
from generator import *
from heuristic import *

# The 'node' and 'cut' variables store, respectively,
# the number of nodes visited throughout the program
# and the number of times the tree was subjected to
# alpha-beta pruning.

node = 0
cut = 0
transposition_table = {}
first_search = {}

# The transposition table will function as a cache that holds
# previously evaluated positions' best move, which avoids
# spending resources on analysing all options from that point on.


class hawkins:

    def search(self, mx, player, depth, last_move, castling_chance):
        global transposition_table
        global first_search
        global node
        global cut

        if player == "Black":
            maximize = True
        else:
            maximize = False

        quiet = False
        
        # This boolean,'quiet', controls whether the engine performs a
        # Quiescence Search at the end of the Minimax Search, looking to evaluate
        # less 'noisy' positions per se, where less pieces seem to be hanging.
        # Enabling this option will result a critical loss of performance.

        starting_point = time.time()
        for level in range(1, depth + 1):
            
            # Iterative deepening, perfect when dealing with time constrains
            # as it allow us to store the best move from previous iterations
            # and evaluate that same position first in the next one, 
            # which makes the pruning even more agressive.

            print(len(transposition_table))
            best_move = hawkins.minimax(self, mx, level, -1*10**5, 1*10**5, maximize, castling_chance, last_move, quiet)[1]
            print(len(transposition_table))
            #print(best_move)
            if time.time() - starting_point >= 10:
                transposition_table = {}
                return best_move
            else:
                first_search[mx] = best_move
                
                # Storing the best move found in the transposition table,
                # in order to evaluate it first and hopefuly discard
                # other options sooner.
        transposition_table = {}
        return best_move

    def q_search(self, mx, depth, alpha, beta, maximizing_player, castling_chance, last_move):

        global transposition_table
        global first_search
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

            # A Negamax Search hybrid, that looks for all possible captures
            # in the given state of the board, stoping when it reaches
            # an certain depth.

            node += 1
            eval = hawkins.q_search(self, capture, depth-1, -beta, -alpha, not maximizing_player, castling_chance, last_move)

            if -eval[0] >= beta:
                cut += 1
                return (beta, mx)
            alpha = max(alpha, -eval[0])   

        return (alpha, mx)

    
    def minimax(self, mx, depth, alpha, beta, maximizing_player, castling_chance, last_move, quiet):
        #print(maximizing_player)
        global node
        global cut
        global first_search
        global transposition_table

        white_pieces = {"P", "R", "K", "Q", "N", "B"}
        black_pieces = {"p", "r", "k", "q", "n", "b"}
        black_castling = [True if x != 0 else False for x in castling_chance][2:]
        white_castling = [True if x != 0 else False for x in castling_chance][:2]
        node += 1

        # We should not waste resources analyzing
        # a position previously evaluated. We must
        # immediately return the best move recorded.

        if mx in transposition_table.keys() and transposition_table[mx][3] >= depth:
            if transposition_table[mx][2] == "Exact":
                if alpha <= transposition_table[mx][0] <= beta:
                    return transposition_table[mx][:2]

            if transposition_table[mx][2] == "Beta":
                if transposition_table[mx][0] > beta:
                    return transposition_table[mx][:2]

            if transposition_table[mx][2] == "Alpha":
                if transposition_table[mx][0] < alpha:
                    return transposition_table[mx][:2]



        if depth == 0:
            if quiet:
               return hawkins.q_search(self, mx, 2, alpha, beta, not maximizing_player, castling_chance, last_move)
            return (points.evaluate(mx), mx)

        if not maximizing_player:

            # Checking if the 'White' castled in this play
            # by looking at the position of its key pieces.
            # Same goes for 'Black' after the 'else' statement.

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

        # Generating all possible moves based
        # on the player's pieces and permission to castle.

        moves_generator = generator.possible_matrix(mx, player, tuple(pieces), last_move, tuple(updated_castling)) 
        possible_states = moves_generator[0]

        if len(possible_states) == 0:
            if rules.is_attacked(mx, player, tuple(pieces), last_move, False):
                if player == "White":
                    return (10000, mx)
                
                # Checkmate must be much more valuable than
                # all the pieces' values combined.

                else:
                    return (-10000, mx)
            return (0, mx)
        
        if mx in first_search.keys():

            # At first, the only move stored in the transposition table
            # is the best move found in the previous iteration.
            # We want to evaluate it again at a deeper search
            # before any other play as it is the most promissing.

            possible_states.insert(0, first_search[mx])

        flag = ""
        temp_alpha = alpha

        if maximizing_player:
            
            max_eval = -1*10**5

            for state in possible_states:

                node += 1
                eval = hawkins.minimax(self, state, depth-1, alpha, beta, False, castling_chance, last_move, quiet)

                if eval[0] > max_eval:
                    max_eval = eval[0]
                    chosen = state
                alpha = max(alpha, eval[0])

                if beta <= alpha:
                    # Pruning
                    flag = "Beta"
                    cut += 1
                    break

            if flag != "Beta":
                if temp_alpha == alpha:
                    flag = "Alpha"
                elif flag == "":
                    flag = "Exact"

            transposition_table[mx] = (max_eval, chosen, flag, depth)
            return (max_eval, chosen)

        else:

            min_eval = 1*10**5

            for state in possible_states:
                
                node += 1
                eval = hawkins.minimax(self, state, depth-1, alpha, beta, True, castling_chance, last_move, quiet)

                if eval[0] < min_eval:
                    min_eval = eval[0]
                    chosen = state
                beta = min(beta, eval[0])

                if beta <= alpha:
                    # Pruning
                    flag = "Beta"
                    cut += 1
                    break

            if flag != "Beta":
                if temp_alpha == alpha:
                    flag = "Alpha"
                elif flag == "":
                    flag = "Exact"

            transposition_table[mx] = (min_eval, chosen, flag, depth)
            return (min_eval, chosen)


generator = generator()
points = points()
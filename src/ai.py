import random
import time
import math
import copy
from generator import generator
from heuristic import evaluate
from rules import is_attacked, check_order

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


class Hawkins:

    def search(self, mx, player, depth, last_move, castling_chance):
        """
        Performs iterative, deeper Minimax Searches
        while there are computational resources left.

        :param mx: board's state.
        :param player: the color of AI's pieces.
        :param depth: max search depth.
        :param last_move: the last move played.

        :param castling_chance: an array that holds
        information on whether each player can castle.
        """
        global transposition_table
        global first_search
        global node
        global cut

        if player == "Black":
            maximize = True
        else:
            maximize = False

        starting_point = time.time()
        for level in range(1, depth + 1):
            
            # Iterative deepening, perfect when dealing with time constrains
            # as it allow us to store the best move from previous iterations
            # and evaluate that same position first in the next one, 
            # which makes the pruning even more agressive.

            search = Hawkins.minimax(self, mx, level, -1*10**5, 1*10**5, maximize, castling_chance, last_move)
            best_move = search[1]
            if search[0] == 10000:
                return best_move

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

    
    def minimax(self, mx, depth, alpha, beta, maximizing_player, castling_chance, last_move):
        """
        A Minimax Search that makes use of
        multiple alpha-beta pruning extensions,
        neat move-ordering and many optimization techniques.

        :param mx: board's state.
        :param depth: max search depth.
        :param alpha: alpha cutoff value.
        :param beta: beta cutoff value.

        :param maximizing_player: the evaluation function
        returns positive values when the black pieces are
        favored, and negative scores when the white pieces
        take the advantage. With that in mind, depending on
        the AI's pieces we can tell the search to maximize,
        or to minimize each given decision (black to maximize,
        white to minimize).

        :param castling_chance: an array that holds
        information on whether each player can castle.

        :param last_move: the last move played.
        """

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
            return (evaluate(mx), mx)

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
            if is_attacked(mx, player, tuple(pieces), last_move, False):
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
                eval = Hawkins.minimax(self, state, depth-1, alpha, beta, False, castling_chance, last_move)

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
                eval = Hawkins.minimax(self, state, depth-1, alpha, beta, True, castling_chance, last_move)

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



class Tree:

    def __init__(self, board):
        """
        Tree constructor.
        """

        self.board = board
        self.visits = 0
        self.score = 0
        self.children = []

class Pluto:

    def search(self, mx, player, last_move, castling_chance):
        """
        Monte Carlo Tree Search algorithm, that uses
        random rollouts and no previous knowledge of
        the game to play.

        :param mx: board's state.
        :param player: the color of AI's pieces.
        :param last_move: the last move played.
        :param castling_chance: an array that holds
        information on whether each player can castle.
        """

        depth = 3

        #Cutoff depth

        starting_point = time.time()
        root = Tree(mx)

        while time.time() - starting_point <= 2:

            leaf = Pluto.expand(self, root.board, player, root, last_move, castling_chance)
            result = Pluto.rollout(self, player, leaf, last_move, castling_chance, depth)
            Pluto.backpropagate(self, leaf, root, result)

        return Pluto.best_child(self, root).board

    def expand(self, mx, player, root, last_move, castling_chance):
        """
        On this phase, we expand the tree by adding
        to the root its child nodes and we select
        one of those states to be explored.

        :param mx: board's state
        :param player: the color of AI's pieces.
        :param root: root object.
        :param last_move: the last move played.
        :param castling_chance: an array that holds
        information on whether each player can castle.
        """

        white_pieces = {"P", "R", "K", "Q", "N", "B"}
        black_pieces = {"p", "r", "k", "q", "n", "b"}

        black_castling = [True if x != 0 else False for x in castling_chance][2:]
        white_castling = [True if x != 0 else False for x in castling_chance][:2]

        if player == "White":
            pieces, updated_castling = white_pieces, white_castling
        else:
            pieces, updated_castling = black_pieces, black_castling

        if len(root.children) == 0:
            matrices  = generator.possible_matrix(mx, player, tuple(pieces), last_move, tuple(updated_castling))[0]
            root.children = [Tree(matrix) for matrix in matrices]
        
        for child in root.children:
            if child.visits == 0:

                # We must visit the nodes that haven't
                # been explored yet first.

                return child

        # In case every single node has been chosen
        # atleast once, then we must choose the one
        # that seems to have the most potential.

        return Pluto.expansion_choice(self, root)

    def rollout(self, player, leaf, last_move, castling_chance, depth):
        """
        Random rollout phase.

        :param player: color of AI's pieces.
        :param leaf: child node.
        :param last_move: the last move played.
        :param castling chance: an array that holds
        information on whether each player can castle.
        :param depth: max_depth search.
        """
        level = 0
        mx = leaf.board
        
        white_pieces = {"P", "R", "K", "Q", "N", "B"}
        black_pieces = {"p", "r", "k", "q", "n", "b"}
        
        black_castling = [True if x != 0 else False for x in castling_chance][2:]
        white_castling = [True if x != 0 else False for x in castling_chance][:2]

        if player == "White":
            swap = 0
        else:
            swap = 1

        while Pluto.material_left(self, mx) and level <= depth:

            if swap == 1: # White is playing
                possible_states = generator.possible_matrix(mx, "White", tuple(white_pieces), last_move, tuple(white_castling))[0]

                if len(possible_states) == 0:
                    if is_attacked(mx, "White", tuple(white_pieces), last_move, False):
                        return 10000
                    return 0

                if len(possible_states) == 1:
                    mx =  possible_states[0]
                else:
                    choice = random.randrange(0, len(possible_states))
                    mx = possible_states[choice]

                if True in white_castling:
                    if mx[7*8+4] != "K":
                        white_castling = [False, False]
                    else:
                        if white_castling[0] == True and mx[7*8] != "R":
                            black_castling[0] = False
                        if black_castling[1] == True and mx[7*8 + 7]!= "R":
                            black_castling[1] = False
                            white_castling[0] = False
                        if white_castling[1] == True and mx[7*8 + 7]!= "R":
                            white_castling[1] = False

            elif swap == 0: # Black is playing

                if True in black_castling:
                    if mx[4] != "k":
                        black_castling = [False, False]
                    else:
                        if black_castling[0] == True and mx[0] != "r":
                            black_castling[0] = False
                        if black_castling[1] == True and mx[7]!= "r":
                            black_castling[1] = False

                possible_states = generator.possible_matrix(mx, "Black", tuple(black_pieces), last_move, tuple(black_castling))[0]
                
                if len(possible_states) == 0:
                    if is_attacked(mx, "Black", tuple(black_pieces), last_move, False):

                        return -10000

                    return 0
                if len(possible_states) == 1:
                    mx =  possible_states[0]
                else:
                    choice = random.randrange(0, len(possible_states))
                    mx = possible_states[choice]
                    
            level += 1
            swap += 1
            swap = swap % 2
        
        if player == "White":
            return -evaluate(mx)
        return evaluate(mx)
        
    def material_left(self, mx):
        """
        Resumes the random rollout while
        there are sufficient pieces left.
        """

        king_counter = 0
        minor_counter = 0

        for i in mx:
            if i.upper() in "K":
                king_counter +=1
            if i != "-" and i.upper() not in "K":
                minor_counter +=1

        if king_counter != 2:
            return False
        else:
            return True

    def backpropagate(self, leaf, root, result):
        """
        Updates our prospects stats
        after the rollout phase ends.
        """

        leaf.score += result
        leaf.visits += 1
        root.visits += 1

    def calculate_score(self, score, child_visits, parent_visits, c):

        return score / child_visits + c * math.sqrt(math.log(parent_visits) / child_visits)

    def expansion_choice(self, root): 
        """
        Returns most promising node
        according to the UCB1 formula.
        """

        threshold = -1*10**6

        for child in root.children:

            potential = Pluto.calculate_score(self, child.score, child.visits, root.visits, 1.414)
            if potential > threshold:
                choice = child
                threshold = potential
                
        return choice

        
    def best_child(self,root):
        """
        Returns most promising node
        based on its number of visits.
        """

        threshold = -1*10**6

        for child in root.children:

            if child.visits > threshold:
                win_choice = child
                threshold = child.visits

        return win_choice


generator = generator()
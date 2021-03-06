import random
import math
import copy
from generator import *
from heuristic import *

white_pieces = {"P", "R", "K", "Q", "N", "B"}
black_pieces = {"p", "r", "k", "q", "n", "b"}
transposition_table = {}


class tree:
    def __init__(self, board):
        self.board = board
        self.visits = 0
        self.score = 0
        self.children = []
class mcts:
    def search(self, mx, player, last_move, castling_chance):
        global transposition_table
        depth = 3
        root = tree(mx)
        for _ in range(3000):
            leaf = mcts.expand(self, root.board, player, root, last_move, castling_chance)
            result = mcts.rollout(self, leaf, last_move, castling_chance, depth)
            mcts.backpropagate(self, leaf, root, result)
        transposition_table = {}
        return mcts.best_child(self, root).board

    def expand(self, mx, player, root, last_move, castling_chance):
        global white_pieces
        global black_pieces
        black_castling = [True if x != 0 else False for x in castling_chance][2:]
        plays = []
        matrices = generator.possible_matrix(mx, player, black_pieces, last_move, black_castling)[0] #all possible plays
        if root.visits == 0:
            for matrix in matrices:
                child_node = tree(matrix)
                plays.append(child_node)
            for child in plays:
                root.children.append(child) #create child_nodes in case they havent been created yet
        for child in root.children:
            if child.visits == 0:
                return child #first iterations of the loop
        return mcts.expansion_choice(self, root) #choose the one with most potential

    def rollout(self, leaf, last_move, castling_chance, depth):
        global transposition_table
        global white_pieces
        global black_pieces
        mx = leaf.board
        swap = 1
        level = 0 
        black_castling = [True if x != 0 else False for x in castling_chance][2:]
        white_castling = [True if x != 0 else False for x in castling_chance][:2]
        possible_states = generator.possible_matrix(mx, "White", white_pieces, last_move, white_castling)[0]
        while mcts.material_left(self, mx) and level <= depth:
            if swap == 1: # "White's" playing
                if len(possible_states) == 0:
                    if rules.is_attacked(mx, "White", white_pieces, last_move, 0):
                        transposition_table[mx] = 300
                        return 300
                    transposition_table[mx] = 0
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

            elif swap == 0: # "Black" playing
                if True in black_castling:
                    if mx[4] != "k":
                        black_castling = [False, False]
                    else:
                        if black_castling[0] == True and mx[0] != "r":
                            black_castling[0] = False
                        if black_castling[1] == True and mx[7]!= "r":
                            black_castling[1] = False

                possible_states = generator.possible_matrix(mx, "Black", black_pieces, last_move, black_castling)[0]
                if len(possible_states) == 0:
                    print(level)
                    if rules.is_attacked(mx, "Black", black_pieces, last_move, 0):
                        transposition_table[mx] = -300
                        return -300
                    transposition_table[mx] = 0
                    return 0
                if len(possible_states) == 1:
                    mx =  possible_states[0]
                else:
                    choice = random.randrange(0, len(possible_states))
                    mx = possible_states[choice]
            level += 1
            swap += 1
            swap = swap % 2
        if mx in transposition_table.keys():
            return transposition_table[mx]
        transposition_table[mx] = points.evaluate(mx)
        #print(transposition_table[mx]) #this is a placeholder for a evaluation function
        return transposition_table[mx]

    def backpropagate(self, leaf, root, result): # updating our prospects stats
        leaf.score += result
        leaf.visits += 1
        root.visits += 1

    def material_left(self, mx):
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


    def calculate_score(self, score, child_visits, parent_visits, c): #UCB1
        return score / child_visits + c * math.sqrt(math.log(parent_visits) / child_visits)

    def expansion_choice(self, root): #returns most promising node
        threshold = -1*10**6
        for child in root.children:
            potential = mcts.calculate_score(self, child.score, child.visits, root.visits, 1.414)
            #print(potential)
            #print(potential > threshold)
            if potential > threshold:
                #print("reached")
                choice = child
                threshold = potential
        #print(mcts.calculate_score(self, choice.score, choice.visits, root.visits, 1.414), "here")
        return choice

    def best_child(self,root):
        threshold = -1*10**6
        #print("we_got_here")
        for child in root.children:
            print(points.evaluate(child.board))
            if child.visits > threshold:
                win_choice = child
                threshold = child.visits
        #print("winning", points.evaluate(win_choice.board))
        return win_choice


generator = generator()
points = points()
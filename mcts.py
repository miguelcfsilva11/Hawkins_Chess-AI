import random
import math
import copy
from generator import *

white_pieces = {"P", "R", "K", "Q", "N", "B"}
black_pieces = {"p", "r", "k", "q", "n", "b"}



class tree:
    def __init__(self, board):
        self.board = board
        self.visits = 0
        self.score = 0
        self.children = []
class mcts:
    def search(self, mxs, player, last_move):
        root = tree(mxs)
        for _ in range(30):
            leaf = mcts.expand(self, root.board, player, root, last_move)
            result = mcts.rollout(self, leaf, last_move)
            mcts.backpropagate(self, leaf, root, result)
        return mcts.best_child(self, root).board

    def expand(self, mxs, player, root, last_move):
        global white_pieces
        global black_pieces

        plays = []
        if player == "Black":
            matrices = generator.possible_matrix(mxs, player, black_pieces, last_move)[0] #all possible plays
        if player == "White":
            matrices = generator.possible_matrix(mxs, player, white_pieces, last_move)[0] #all possible plays
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

    def rollout(self, leaf, last_move):
        global white_pieces
        global black_pieces
        mxs = leaf.board
        swap = 1
        while mcts.material_left(self, mxs):
            if swap == 1: # "White's" playing
                possible_states = generator.possible_matrix(mxs, "White", white_pieces, last_move)[0]
                if len(possible_states) == 0:
                    if rules.is_attacked(mxs, "White", white_pieces, last_move):
                        return 1
                    return 0
                if len(possible_states) == 1:
                    mxs =  possible_states[0]
                else:
                    choice = random.randrange(0, len(possible_states))
                    mx = possible_states[choice]
            elif swap == 0: # "Black" playing
                possible_states = generator.possible_matrix(mxs, "Black", black_pieces, last_move)[0]
                if len(possible_states) == 0:
                    if rules.is_attacked(mxs, "Black", black_pieces, last_move):
                        return -1
                    return 0
                if len(possible_states) == 1:
                    mxs =  possible_states[0]
                else:
                    choice = random.randrange(0, len(possible_states))
                    mxs = possible_states[choice]
            swap += 1
            swap = swap % 2
        return 0

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
        if minor_counter == 0:
            return True

    def calculate_score(self, score, child_visits, parent_visits, c): #UCB1
        return score / child_visits + c * math.sqrt(math.log(parent_visits) / child_visits)

    def expansion_choice(self, root): #returns most promising node
        threshold = -1*10**6
        for child in root.children:
            potential = mcts.calculate_score(self, child.score, child.visits, root.visits, 1.414)
            if potential > threshold:
                choice = child
                threshold = potential
        return choice

    def best_child(self,root):
        threshold = -1*10**6
        for child in root.children:
            if child.visits > threshold:
                win_choice = child
                threshold = child.visits
        return win_choice

generator = generator()
#todo create script that generates possible matrix
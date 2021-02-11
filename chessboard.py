import math
import random
import os
from copy import deepcopy
from generator import *
from mcts import *
from rules import *
from ui import *

pieces_taken = {}

white_pieces = {"P", "R", "K", "Q", "N", "B"}
black_pieces = {"p", "r", "k", "q", "n", "b"}

mx=[["r","n","b","q","k","b","n","r"],
    ["p","p","p","p","p","p","p","p"],
    ["-","-","-","-","-","-","-","-"],
    ["-","-","-","-","-","-","-","-"],
    ["-","-","-","-","-","-","-","-"],
    ["-","-","-","-","-","-","-","-"],
    ["P","P","P","P","P","P","P","P"],
    ["R","N","B","Q","K","B","N","R"]]


castling_chance = True
moves_log = ["Start:"] #placeholder move
      
playable = True
class board:
    def __init__(self, board = "current"):
        self.player1 = "White"
        self.player2 = "Black"

    def endgame(self):
        global playable
        global mx
        if playable == False:
            repeat = input("Want to play again?\nY/N?: ")
            if repeat.upper() in "Y":
                playable = True
                mx=[["r","n","b","q","k","b","n","r"],
                    ["p","p","p","p","p","p","p","p"],
                    ["-","-","-","-","-","-","-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    ["-","-","-","-","-","-","-","-"],
                    ["P","P","P","P","P","P","P","P"],
                    ["R","N","B","Q","K","B","N","R"]]
                board.output_matrix(mx)
            else:
                print("Bye!")

    def output_matrix(self,mx):
        os.system('cls' if os.name == 'nt' else 'clear') # nt is for Windows, otherwise Linux or Mac
        printable_matrix = ("\t8 {0}\n\t7 {1}\n\t6 {2}\n"
                             "\t5 {3}\n\t4 {4}\n\t3 {5}\n "
                              "\t2 {6}\n\t1 {7}\n\t {8}\t{9}{10}{11}{12}{13}{14}{15}").format(mx[0], mx[1], mx[2], mx[3],
                                                    mx[4], mx[5], mx[6], mx[7],"   a", " b", "    c","    d","    e","    f","    g","    h")
        print("\n" + printable_matrix + "\n")
    
    def final(self,mx, player):
        global playable
        possible_draw = 1
        possible_win = 1
        if rules.is_checkmate(mx, player):
            playable = 0
            message = ("Checkmate! {0} wins!").format(player)
            print(message)
        for i in mx:
            for k in i:
                if k != "-":
                    if k.upper() not in "K":
                        possible_draw = 0
        if possible_draw == 1:
            playable = 0
            message = ("It's a Tie!")
            print(message)
        
        
    def gameplay(self):
        global mx
        global pieces_taken
        global playable
        global moves_log
        global white_pieces
        global black_pieces

        os.system('cls' if os.name == 'nt' else 'clear')
        print("\nHey! Let's play Chess! What's your first move?\nUse algebraic notation to tell us that! For example, writing 'e2e3'" 
        "\nwould move your pawn from e2 to e3. To quit write the word 'stop'."
              "\nTake a look at the board!\n")

        printable_matrix = ("\t8 {0}\n\t7 {1}\n\t6 {2}\n"
                             "\t5 {3}\n\t4 {4}\n\t3 {5}\n "
                              "\t2 {6}\n\t1 {7}\n\t {8}\t{9}{10}{11}{12}{13}{14}{15}").format(mx[0], mx[1], mx[2], mx[3],
                                                    mx[4], mx[5], mx[6], mx[7],"   a", " b", "    c","    d","    e","    f","    g","    h")
        print("\n" + printable_matrix + "\n")

        while playable:
            try:
                human_move = input("Choose your position: ")
                if human_move.upper() in "STOP":
                    break
                else:
                    pos = list(human_move)
                    print(pos)
                    initial_pos = (8-int(pos[1]), movements.alge(pos[0])-1)
                    final = (8-int(pos[3]), movements.alge(pos[2])-1)
                    result = rules.check_order(mx, initial_pos, final, self.player1, moves_log[-1])
                    if not result[0] or initial_pos == final or mx[final[0]][final[1]] in white_pieces:
                        print("Illegal move, chief!")
                        continue
                    moves_log.append(human_move)
                    if result[1] == "en_passant":
                        mx = generator.move(initial_pos, final, self.player1, "en_passant", mx)
                    elif result[1] == "promotion":
                        mx = generator.move(initial_pos, final, self.player1, "promotion", mx)
                    else:
                        mx = generator.move(initial_pos, final, self.player1, "step", mx)
                    board.final(mx, self.player1)
                    board.output_matrix(mx)
                    if playable == False:
                        board.endgame()
                    else:
                        print("Hawkins is thinking...")
                        mx = mcts.search(mx, self.player2, moves_log[-1])
                        board.final(mx, self.player2)
                        board.endgame()
                        if playable == False:
                            continue
                        else:
                            board.output_matrix(mx)
            except Exception as e:
                print(e)
                print("That's not valid!")

colors = colors()
backgrounds = backgrounds()
styles = styles()
rules = rules()
mcts = mcts()
board = board()
board.gameplay()

#todo as of now, this is a copy of tic-tac-toe. Tommorrow, we'll make this functional.
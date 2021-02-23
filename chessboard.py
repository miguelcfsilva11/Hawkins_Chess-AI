import math
import random
import os
from copy import deepcopy
from generator import *
from mcts import *
from rules import *
from util import *

pieces_taken = {}

board_pieces = {
    
    'R': colors.LIGHT + '♜ ' + colors.RESET,
    'N': colors.LIGHT + '♞ ' + colors.RESET,
    'B': colors.LIGHT + '♗ ' + colors.RESET,
    'Q': colors.LIGHT + '♕ ' + colors.RESET,
    'K': colors.LIGHT + '♔ ' + colors.RESET,
    'P': colors.LIGHT + '♙ ' + colors.RESET,
    # Black
    'r': colors.DARK + '♜ ' + colors.RESET,
    'n': colors.DARK + '♞ ' + colors.RESET,
    'b': colors.DARK + '♝ ' + colors.RESET,
    'q': colors.DARK + '♛ ' + colors.RESET,
    'k': colors.DARK + '♚ ' + colors.RESET,
    'p': colors.DARK + '♙ ' + colors.RESET,
    "-": "  "
}
moves_log = ["Start"] #placeholder move
mx = "rnbqkbnrpppppppp--------------------------------PPPPPPPPRNBQKBNR"

castling_chance = True
playable = True

class board:

    def __init__(self, board = "current"):
        self.player1 = "White"
        self.player2 = "Black"
        self.player1pieces = {"P", "R", "K", "Q", "N", "B"}
        self.player2pieces = {"p", "r", "k", "q", "n", "b"}

    def endgame(self):
        global playable
        global mx
        if playable == False:
            repeat = input("Want to play again?\nY/N?: ")
            if repeat.upper() in "Y":
                playable = True
                mx = "rnbqkbnrpppppppp--------------------------------PPPPPPPPRNBQKBNR"
                board.output_matrix(mx)
            else:
                print("Bye!")

    def output_matrix(self,mx,player):
        #os.system('cls' if os.name == 'nt' else 'clear') # nt is for Windows, otherwise Linux or Mac
        global board_pieces
        if player == "White":
            print("\n\n\n\t\t            " + colors.BOLD + colors.DARK + backgrounds.WHITE + "    Your turn   " + colors.RESET + "\n")
        else:
            print("\n\n\n\t\t            " + colors.BOLD + colors.WHITE + backgrounds.BLACK + "  Hawkins' turn " + colors.RESET + "\n")
        for row in range(8):
            if row%2 == 0:
                current_color = "white"
            else:
                current_color = "black"
            line = list(mx[0+8*row: 8 +8*row])
            for piece in range(len(line)):
                if current_color == "white":
                    line[piece] = backgrounds.LIGHT + board_pieces[line[piece]] + colors.RESET
                    current_color = "black"
                    continue
                elif current_color == "black":
                    line[piece] = backgrounds.DARK + board_pieces[line[piece]] + colors.RESET
                    current_color = "white"
                    continue
            line = "".join(line)
            print("                          " + colors.BOLD + colors.GRAY + str(8-row) + colors.RESET +  " " + line)
        print(colors.BOLD + colors.GRAY + "                            a b c d e f g h" + colors.RESET)

    def final(self,mx, player, pieces, last_move):
        global playable
        possible_draw = 1
        possible_win = 1
        in_check= rules.is_attacked(mx, player, pieces, last_move)
        if in_check:
            print("Check!")
        valid_moves = generator.possible_matrix(mx, player, pieces, last_move)[1]
        print(valid_moves)
        if len(valid_moves) == 0 and in_check:
            print("Checkmate!")
            playable = 0
        if len(valid_moves) == 0 and not in_check:
            print("Stalemate!")
            playable = 0
        for i in mx:
            if i != "-":
                if i.upper() not in "K":
                    possible_draw = 0
        if possible_draw == 1:
            playable = 0
            message = ("It's a Tie!")
            print(message)
        
    def help_me(self):
        os.system('cls' if os.name == 'nt' else 'clear') # nt is for Windows, otherwise Linux or Mac
        print("\n\n\n\n\t        Hey! Let's play Chess! What's your move?\n\n" + colors.RESET + "       Use algebraic notation to tell us that! For example, writing 'e2e3'" 
        "\n       would move your pawn from e2 to e3. To quit write the word 'stop'."
              "\n       Type 'castle' in case you want to make that play.\n       Take a look at the board and do your best!\n") 
        choice = input("\t        Understood? Type " + colors.BOLD + "anything" + colors.RESET + " to resume the game!\n\n\t\t\t    ")
        board.output_matrix(mx, "White") 

    def gameplay(self):
        global mx
        global pieces_taken
        global playable
        global moves_log

        board.output_matrix(mx, "White")

        while playable:
            try:
                human_move = input(colors.BOLD + "\n\t\t          ┏━━━━━━━━━━━━━━━━━━\n" + "\t\t            Make your move: ")
                if human_move.upper() in "STOP":
                    break
                if human_move.upper() in "HELP":
                    board.help_me()
                else:
                    pos = list(human_move)
                    initial_pos = (8-int(pos[1]), movements.alge(pos[0])-1)
                    final = (8-int(pos[3]), movements.alge(pos[2])-1)
                    result = rules.check_order(mx, initial_pos, final, self.player1, moves_log[-1])
                    valid_moves = generator.possible_matrix(mx, "White", self.player1pieces, moves_log[-1])[1]
                    if human_move not in valid_moves or initial_pos == final or mx[final[0]*8 + final[1]] in self.player1pieces:
                        board.output_matrix(mx, "White")
                        print(colors.BOLD + "\n\t\t          Illegal move, chief!")
                        continue
                    moves_log.append(human_move)
                    if result[1] == "en_passant":
                        mx = generator.move(initial_pos, final, self.player1, "en_passant", mx)
                    elif result[1] == "promotion":
                        mx = generator.move(initial_pos, final, self.player1, "promotion", mx)
                    else:
                        mx = generator.move(initial_pos, final, self.player1, "step", mx)
                    board.final(mx, self.player2, self.player2pieces, moves_log[-1])
                    board.output_matrix(mx, "Black")
                    if playable == False:
                        board.endgame()
                    else:
                        print(colors.BOLD + "\n\t\t          ┏━━━━━━━━━━━━━━━━━━\n" +  colors.BLINKING + "\t\t            Hawkins' move... " + colors.RESET)
                        mx = mcts.search(mx, self.player2, moves_log[-1])
                        board.final(mx, self.player1, self.player1pieces, moves_log[-1])
                        board.endgame()
                        if playable == False:
                            continue
                        else:
                            board.output_matrix(mx, "White")
            except Exception as e:
                board.output_matrix(mx, "White")
                print(e)
                print(colors.BOLD + "\n\t\t           That's not valid!")
                continue

colors = colors()
backgrounds = backgrounds()
rules = rules()
mcts = mcts()
board = board()

if __name__ == "__main__":
    board.gameplay()

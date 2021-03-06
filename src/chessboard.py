import math
import random
import os
#import sys
from gamelists import game_moves
from copy import deepcopy
from generator import *
from mcts import *
from rules import *
from util import *

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
san_moves_log = ["Start"] #placeholder move
mx = "rnbqkbnrpppppppp--------------------------------PPPPPPPPRNBQKBNR"
castling_chance = ["WhiteL", "WhiteR", "BlackL", "BlackR"]
playable = True
in_check = False

class board:

    def __init__(self, board = "current"):
        self.player1 = "White"
        self.player2 = "Black"
        self.player1pieces = {"P", "R", "K", "Q", "N", "B"}
        self.player2pieces = {"p", "r", "k", "q", "n", "b"}

    def endgame(self):
        global playable
        global in_check
        global moves_log
        global castling_chance
        global mx
        if playable == False:
            repeat = input("Want to play again?\nY/N?: ")
            if repeat.upper() in "Y":
                moves_log = ["Start"] #placeholder move
                mx = "rnbqkbnrpppppppp--------------------------------PPPPPPPPRNBQKBNR"
                castling_chance = ["WhiteL", "WhiteR", "BlackL", "BlackR"]
                playable = True
                in_check = False
                board.output_matrix(mx, "White")
            else:
                print("Bye!")
    def flags_reset(self, flags):
        for state in flags.keys():
            flags[state] = False

    def convert_to_san(self, move, piece, capture_flag, check_flag, ambiguous_flag):
        san_move = ""
        if piece == "P":
            san_move =  move[2:]
            if capture_flag:
                san_move = move[0] +  "x" + san_move
            if check_flag:
                san_move += "+"
            return san_move
        else:
            san_move = piece + move[2:]
            if capture_flag:
                san_move = piece + "x" + move[2:]
            if check_flag:
                san_move = san_move + "+"
            if ambiguous_flag:
                san_move = san_move[:1] + move[0] + san_move[1:]
            return san_move


    def output_matrix(self,mx,player):
        #os.system('cls' if os.name == 'nt' else 'clear') # nt is for Windows, otherwise Linux or Mac
        global board_pieces
        if player == "White":
            print("\n\n\n" + paddings.BIG_PAD + colors.BOLD + colors.DARK + backgrounds.WHITE + "    Your turn   " + colors.RESET + "\n")
        else:
            print("\n\n\n" + paddings.BIG_PAD + colors.BOLD + colors.WHITE + backgrounds.BLACK + "  Hawkins' turn " + colors.RESET + "\n")
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
            print(paddings.GAME_PAD + colors.BOLD + colors.GRAY + str(8-row) + colors.RESET +  " " + line)
        print(colors.BOLD + colors.GRAY + paddings.GAME_PAD + "  a b c d e f g h" + colors.RESET)

    def final(self,mx, player, pieces, last_move):
        global playable
        global castling_chance
        global in_check
        possible_draw = 1
        possible_win = 1
        if player == "White":
            player_castling = [True if x != 0 else False for x in castling_chance][:2]
        else:
            player_castling = [True if x != 0 else False for x in castling_chance][2:]
        in_check= rules.is_attacked(mx, player, pieces, last_move, False)
        if in_check:
            print("Check!")
        valid_moves = generator.possible_matrix(mx, player, pieces, last_move, player_castling)[1]
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

        print("\n\n\n\n" + paddings.CENTER_PAD + "Hey! Let's play Chess! What's your move?\n\n" + colors.RESET + paddings.MIN_PAD +
        "Use algebraic notation to tell us that! For example, writing 'e2e3'\n" + paddings.MIN_PAD + 
        "would move your pawn from e2 to e3. To quit write the word 'stop'.\n" + paddings.MIN_PAD +
        "Type 'castle' in case you want to make that play.\n" + paddings.MIN_PAD + "Take a look at the board and do your best!\n") 

        choice = input(paddings.CENTER_PAD + "Understood? Type " + colors.BOLD + "anything" + colors.RESET + " to resume the game!\n\n" + paddings.BIG_PAD)
        board.output_matrix(mx, self.player1) 
        
    def gameplay(self):
        global mx
        global playable
        global moves_log
        global castling_chance
        board.output_matrix(mx, "White")
        opening_state = True
        sample_text = "d4"
        round = 0
        flags = {"capture_flag": False, "check_flag": False, "ambiguous_flag": False}

        while playable:
            try:
                player_castling = [True if x != 0 else False for x in castling_chance]
                human_move = input(colors.BOLD + "\n" + paddings.MID_PAD + "┏━━━━━━━━━━━━━━━━━━\n" + paddings.BIG_PAD +"Make your move: ")
                if human_move.upper() in "STOP":
                    break
                elif human_move.upper() in "HELP":
                    board.help_me()
                elif human_move.upper() in "CASTLEL":
                    valid_moves = generator.possible_matrix(mx, self.player1, self.player1pieces, moves_log[-1], player_castling[:2])[1]
                    if human_move in valid_moves:
                        mx = generator.castle(mx, self.player1, "left")
                        moves_log.append("O-O")
                    else:
                        board.output_matrix(mx, self.player1)
                        print(colors.BOLD + "\n"+ paddings.MID_PAD + "Illegal move, chief!")
                        continue
                elif human_move.upper() in "CASTLER":
                    valid_moves = generator.possible_matrix(mx, self.player1, self.player1pieces, moves_log[-1], player_castling[:2])[1]
                    if human_move in valid_moves:
                        mx = generator.castle(mx, self.player1, "right")
                        moves_log.append("O-O-O")
                    else:
                        board.output_matrix(mx, self.player1)
                        print(colors.BOLD + "\n" + paddings.MID_PAD + "Illegal move, chief!")
                        continue
                else:
                    pos = list(human_move)
                    initial_pos = (8-int(pos[1]), movements.alge(pos[0])-1)
                    final = (8-int(pos[3]), movements.alge(pos[2])-1)
                    result = rules.check_order(mx, initial_pos, final, self.player1, moves_log[-1])
                    valid_moves = generator.possible_matrix(mx, self.player1, self.player1pieces, moves_log[-1], player_castling)[1]
                    if human_move not in valid_moves or initial_pos == final or mx[final[0]*8 + final[1]] in self.player1pieces:
                        board.output_matrix(mx, self.player1)
                        print(colors.BOLD + "\n" + paddings.MID_PAD + "Illegal move, chief!")
                        continue
                    if mx[initial_pos[0]*8 + initial_pos[1]] == "P":
                        piece_moved = "P"
                    else:
                        piece_moved = mx[initial_pos[0]*8 + initial_pos[1]]
                        possible_pieces = [move for move in valid_moves if move[2:] == human_move[2:]]
                        for move in possible_pieces:
                            move_starting_point = list(move)
                            pos_start = (8-int(move_starting_point[1]), movements.alge(move_starting_point[0])-1)
                            if pos_start != initial_pos and mx[pos_start[0]*8 + pos_start[1]] == piece_moved:
                                flags["ambiguous_flag"] = True
                    if rules.is_attacked(mx, self.player2, self.player2pieces, moves_log[-1], False):
                        flags["check_flag"] = True
                    if result[1] == "en_passant":
                        mx = generator.move(initial_pos, final, self.player1, "en_passant", mx, "letter")
                        flags["capture_flag"] = True
                    elif result[1] == "promotion":
                        choice =  input("Promote to?")
                        while choice.upper() not in "QRNB":
                            choice = input("Choose a valid letter...")
                        mx = generator.move(initial_pos, final, self.player1, "promotion", mx, choice)
                    else:
                        if mx[final[0]*8 + final[1]] not in self.player1pieces and mx[final[0]*8 + final[1]] != "-":
                            flags["capture_flag"] =  True   
                        mx = generator.move(initial_pos, final, self.player1, "step", mx, "letter")
                    moves_log.append(human_move)
                    san_moves_log.append(board.convert_to_san(human_move, piece_moved, flags["capture_flag"], flags["check_flag"], flags["ambiguous_flag"]))
                    #print(moves_log)
                if True in player_castling[:2]:
                    if mx[7*8 + 4] != "K":
                        castling_chance[:2] =  [0,0]
                    else:
                        if player_castling[0] == True and mx[7*8] != "R":
                            castling_chance[0] = 0
                        if player_castling[1] == True and mx[7*8 + 7]!= "R":
                            castling_chance[1] = 0
                board.final(mx, self.player2, self.player2pieces, moves_log[-1])
                board.output_matrix(mx, self.player2)
                if playable == False:
                    board.endgame()
                else:
                    print(colors.BOLD + "\n" +  paddings.MID_PAD + "┏━━━━━━━━━━━━━━━━━━\n" +  colors.BLINKING + paddings.BIG_PAD + "Hawkins' move... " + colors.RESET)
                    if opening_state:
                        fen_state = generator.fen_generator(mx)
                        #print(moves_log[1:])
                        #print(game_moves[0][:round+1])
                        possible_lines = [line for line in game_moves if line[:round*2+1] == san_moves_log[1:]]
                        if len(possible_lines) != 0:
                            choice = random.randrange(0, len(possible_lines))
                            ai_response = possible_lines[choice][1+round*2]
                            san_moves_log.append(ai_response)
                            move = generator.change_notation(fen_state, ai_response)
                            pos = list(move)
                            initial_pos = (8-int(pos[1]), movements.alge(pos[0])-1)
                            final = (8-int(pos[3]), movements.alge(pos[2])-1)
                            result = rules.check_order(mx, initial_pos, final, self.player1, moves_log[-1])
                            if result[1] == "en_passant":
                                mx = generator.move(initial_pos, final, self.player1, "en_passant", mx, "letter")
                            else:
                                mx = generator.move(initial_pos, final, self.player1, "step", mx, "letter")
                        else:
                            #print("Dataset not enough")
                            mx = mcts.search(mx, self.player2, moves_log[-1], castling_chance)
                            opening_state = False
                    else:
                        mx = mcts.search(mx, self.player2, moves_log[-1], castling_chance)
                    if True in player_castling[2:]:
                        if mx[4] != "k":
                            castling_chance[2:] =  [0,0]
                        else:
                            if player_castling[2] == True and mx[0] != "r":
                                castling_chance[3] = 0
                            if player_castling[3] == True and mx[7]!= "r":
                                castling_chance[3] = 0
                    board.final(mx, self.player1, self.player1pieces, moves_log[-1])
                    board.endgame()
                    if playable == False:
                        continue
                    else:
                        board.output_matrix(mx, self.player1)
                        #print(moves_log)
                    board.flags_reset(flags)
                    round += 1
                    if round == 8:
                        opening_state = False
            except Exception as e:
                board.output_matrix(mx, self.player1)
                print(e)
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(exc_type, fname, exc_tb.tb_lineno)
                print(colors.BOLD + "\n" + paddings.MID_PAD + "That's not valid!")
                continue

colors = colors()
backgrounds = backgrounds()
paddings = paddings()
rules = rules()
mcts = mcts()
board = board()

if __name__ == "__main__":
    board.gameplay()

#TODO temos um problema grande com o tratamento dos dados em opening_var. Fazer algo em relação a isso
#TODO limpar os 1. e 2. que se encontram na text file com filtros
#TODO extrair a palavra seguinte (encontrei no stackoverflow uma solução), armazenar numa lista temp
#TODO converter os valores que eles me dão em notação miguel
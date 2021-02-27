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
castling_chance = ["WhiteL", "WhiteR", "BlackL", "BlackR"]
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
                moves_log = ["Start"] #placeholder move
                mx = "rnbqkbnrpppppppp--------------------------------PPPPPPPPRNBQKBNR"
                castling_chance = ["WhiteL", "WhiteR", "BlackL", "BlackR"]
                playable = True
                board.output_matrix(mx, "White")
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
        global castling_chance
        possible_draw = 1
        possible_win = 1
        if player == "White":
            player_castling = [True if x != 0 else False for x in castling_chance][:2]
        else:
            player_castling = [True if x != 0 else False for x in castling_chance][2:]
        in_check= rules.is_attacked(mx, player, pieces, last_move, 0)
        if in_check:
            print("Check!")
        valid_moves = generator.possible_matrix(mx, player, pieces, last_move, player_castling)[1]
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

        print("\n\n\n\n" + paddings.CENTER_PAD + "Hey! Let's play Chess! What's your move?\n\n" + colors.RESET + paddings.MIN_PAD +
        "Use algebraic notation to tell us that! For example, writing 'e2e3'\n" + paddings.MIN_PAD + 
        "would move your pawn from e2 to e3. To quit write the word 'stop'.\n" + paddings.MIN_PAD +
        "Type 'castle' in case you want to make that play.\n" + paddings.MIN_PAD + "Take a look at the board and do your best!\n") 

        choice = input(paddings.CENTER_PAD + "Understood? Type " + colors.BOLD + "anything" + colors.RESET + " to resume the game!\n\n" + paddings.BIG_PAD)
        board.output_matrix(mx, "White") 
        
    def gameplay(self):
        global mx
        global pieces_taken
        global playable
        global moves_log
        global castling_chance
        board.output_matrix(mx, "White")

        while playable:
            try:
                player_castling = [True if x != 0 else False for x in castling_chance]
                human_move = input(colors.BOLD + "\n" + paddings.MID_PAD + "┏━━━━━━━━━━━━━━━━━━\n" + paddings.BIG_PAD +"Make your move: ")
                if human_move.upper() in "STOP":
                    break
                elif human_move.upper() in "HELP":
                    board.help_me()
                elif human_move.upper() in "CASTLEL":
                    valid_moves = generator.possible_matrix(mx, "White", self.player1pieces, moves_log[-1], player_castling[:2])[1]
                    if human_move in valid_moves:
                        mx = generator.castle(mx, "White", "left")
                    else:
                        board.output_matrix(mx, "White")
                        print(colors.BOLD + "\n"+ paddings.MID_PAD + "Illegal move, chief!")
                        continue
                elif human_move.upper() in "CASTLER":
                    valid_moves = generator.possible_matrix(mx, "White", self.player1pieces, moves_log[-1], player_castling[:2])[1]
                    if human_move in valid_moves:
                        mx = generator.castle(mx, "White", "right")
                    else:
                        board.output_matrix(mx, "White")
                        print(colors.BOLD + "\n" + paddings.MID_PAD + "Illegal move, chief!")
                        continue
                else:
                    pos = list(human_move)
                    initial_pos = (8-int(pos[1]), movements.alge(pos[0])-1)
                    final = (8-int(pos[3]), movements.alge(pos[2])-1)
                    result = rules.check_order(mx, initial_pos, final, self.player1, moves_log[-1])
                    valid_moves = generator.possible_matrix(mx, "White", self.player1pieces, moves_log[-1], player_castling)[1]
                    if human_move not in valid_moves or initial_pos == final or mx[final[0]*8 + final[1]] in self.player1pieces:
                        board.output_matrix(mx, "White")
                        print(colors.BOLD + "\n" + paddings.MID_PAD + "Illegal move, chief!")
                        continue
                    moves_log.append(human_move)
                    if result[1] == "en_passant":
                        mx = generator.move(initial_pos, final, self.player1, "en_passant", mx, "letter")
                    elif result[1] == "promotion":
                        choice =  input("Promote to?")
                        while choice.upper() not in "QRKB":
                            choice = input("Choose a valid letter...")
                        mx = generator.move(initial_pos, final, self.player1, "promotion", mx, choice)
                    else:
                        mx = generator.move(initial_pos, final, self.player1, "step", mx, "letter")
  
                if True in player_castling[:2]:
                    if mx[7*8 + 4] != "K":
                        castling_chance[:2] =  [0,0]
                    else:
                        if player_castling[0] == True and mx[7*8] != "R":
                            castling_chance[0] = 0
                        if player_castling[1] == True and mx[7*8 + 7]!= "R":
                            castling_chance[1] = 0

                board.final(mx, self.player2, self.player2pieces, moves_log[-1])
                board.output_matrix(mx, "Black")
                if playable == False:
                    board.endgame()
                else:
                    print(colors.BOLD + "\n" +  paddings.MID_PAD + "┏━━━━━━━━━━━━━━━━━━\n" +  colors.BLINKING + paddings.BIG_PAD + "Hawkins' move... " + colors.RESET)
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
                        board.output_matrix(mx, "White")
                        print(moves_log)
            except Exception as e:
                board.output_matrix(mx, "White")
                print(e)
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

#todo castling, para isso no nosso generator vamos adicionar um parametro chamado castling. Assim a função podera ser chamada tendo em conta isso
#todo mcts tb tera um pequeno update, vamos transpor a informação de castling para o bot.
#todo mcts no rollout vai ter uma validação para ver, caso o valor transposto de castling seja true, se o castling a cada jogada do random playout muda ou nao.
#todo mcts esta validação passará por 2 fases (restante validação no gerador), primeira ver se o valor de castling é possivel, caso tenha mexido alguma das 3 peças chave, passa a ser false.
#todo implementar variavel no mcts tal que se depois de uma jogada der castling, passar a chamar com valores de castling false. Para isso temos de guardar
# numa outra variavel local dentro do random playout para evitar alterar o castling quando o mcts procurar numa leaf diferente (nao ser afetada pelo random playout)

# added step variable to is attacked
# added chance castling to search and generator

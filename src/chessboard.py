import math, random, os, sys

sys.path.insert(0, 'data')

from gamelists import game_moves
from generator import generator
from ai import Hawkins, Pluto
from movements import movements
from rules import is_attacked, check_order
from heuristic import evaluate
from util import *
import time


# Pairing Unicode Pieces with their correspondant letters.

board_pieces = {
    
    'R': colors.LIGHT + '♜ ' + colors.RESET,
    'N': colors.LIGHT + '♞ ' + colors.RESET,
    'B': colors.LIGHT + '♗ ' + colors.RESET,
    'Q': colors.LIGHT + '♕ ' + colors.RESET,
    'K': colors.LIGHT + '♔ ' + colors.RESET,
    'P': colors.LIGHT + '♙ ' + colors.RESET,

    'r': colors.DARK + '♜ ' + colors.RESET,
    'n': colors.DARK + '♞ ' + colors.RESET,
    'b': colors.DARK + '♝ ' + colors.RESET,
    'q': colors.DARK + '♛ ' + colors.RESET,
    'k': colors.DARK + '♚ ' + colors.RESET,
    'p': colors.DARK + '♙ ' + colors.RESET,
    "-": "  "
}

# The string 'Start' will serve as a placeholder
# for our history of moves' arrays. They record
# the moves separately, storing every play both
# in Coordinate and SAN notation.

moves_log = ["Start"]
san_moves_log = ["Start"]

# The variable 'mx' will hold our current game state in
# the form of a string for efficiency purposes.
# The following string represents the initial state of the board.


mx = "rnbqkbnrpppppppp--------------------------------PPPPPPPPRNBQKBNR"

eval_bar = ""
castling_chance = ["WhiteL", "WhiteR", "BlackL", "BlackR"]

opening_state = True
playable = True
in_check = False

class board:

    def __init__(self, player, depth):
        """
        Creating 'board' object that will have
        two distinct players and their respective
        pieces associated to them.

        :param player: pieces that the user wants to play with.
        :param depth: controls the AI's level of difficulty. 
        """

        self.player1 = "White"
        self.player2 = "Black"
        self.player1pieces = {"P", "R", "K", "Q", "N", "B"}
        self.player2pieces = {"p", "r", "k", "q", "n", "b"}

        if player == "Black":

            self.player1, self.player2 = self.player2, self.player1
            self.player1pieces, self.player2pieces = self.player2pieces, self.player1pieces

        self.depth = depth
        board.gameplay(self)

    def endgame(self):
        """
        If the game has ended, presents to
        the user the option of play once again.
        """

        global playable
        global in_check
        global opening_state
        global moves_log
        global san_moves_log
        global eval_bar
        global castling_chance
        global mx

        if playable == False:
            repeat = input("Want to play again?\nY/N?: ")

            if repeat.upper() in "YES":

                # Reseting all variables to their initial value.

                moves_log = ["Start"]
                san_moves_log = ["Start"]
                eval_bar = ""
                mx = "rnbqkbnrpppppppp--------------------------------PPPPPPPPRNBQKBNR"
                castling_chance = ["WhiteL", "WhiteR", "BlackL", "BlackR"]
                opening_state = True
                playable = True
                in_check = False

                self.player1, self.player2 = self.player2, self.player1
                self.player1pieces, self.player2pieces = self.player2pieces, self.player1pieces

                board.output_matrix(self, mx, self.player1)

            else:
                print("Bye!")


    @staticmethod
    def flags_reset(flags):
        """
        Resets any dictionary keys'
        values to False.
        """
        for state in flags.keys():
            flags[state] = False


    @staticmethod
    def convert_to_san(move, piece, capture_flag, check_flag, ambiguous_flag):
        """
        Converts a string that represents a move
        in Coordinate Notation to SAN Notation,
        given the values of the following flags.

        :param move: move that was played in Coordinate Notation
        :param piece: piece that was played.

        :param capture_flag: A boolean value that holds
        information on whether the move was capture.

        :param check_flag: A boolean value that holds
        information on whether the move resulted
        in 'Check'.

        :param ambiguous_flag: A boolean value that holds
        information on whether the final position of
        piece that was played could have been reached
        by other piece of that same kind.
        """
        san_move = ""

        if piece.upper() in "P":
            san_move =  move[2:]
            if capture_flag:
                san_move = move[0] +  "x" + san_move
            if check_flag:
                san_move += "+"
            return san_move

        else:
            san_move = piece.upper() + move[2:]

            if capture_flag:
                san_move = piece.upper() + "x" + move[2:]
            if check_flag:
                san_move = san_move + "+"
            if ambiguous_flag:
                san_move = san_move[:1] + move[0] + san_move[1:]

            return san_move

    @staticmethod
    def get_move(mx, temp_mx):
        """
        Given the board's state before the AI's
        turn to play, and the one after it moves,
        return the play that was made in Coordinate Notation.

        :param mx: current board's state.
        :param temp_mx: board's state before AI's response.
        """

        move = ""
        for i in range(len(mx)):
            if mx[i] != temp_mx[i]:
                row = i//8
                col = i%8
                move += generator.turn_alge(col) + str(8-row)
        return move


    def output_matrix(self, mx, player):
        """
        This function formats the strings that
        contain the game's state into a full-fledged
        chessboard for a more complete experience.

        :param mx: board's state.
        :param player: the one expected to play.
        """

        global board_pieces
        global eval_bar

        os.system('cls' if os.name == 'nt' else 'clear') # nt is for Windows, otherwise Linux or Mac
        eval = evaluate(mx)

        if player == self.player1:
            if player == "White":
                eval = -eval

            white_score = 7 + int((1 + -eval/200) + 0.5)
            black_score = 7 + int((1 + eval/200) + 0.5)

            eval_bar = colors.BOLD + paddings.GAME_PAD + "  " + backgrounds.RED + " "*(min(white_score, 16)) + backgrounds.GREEN_LIGHT + " "*(min(black_score, 16)) + colors.RESET
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
        print(eval_bar)


    @staticmethod
    def final(mx, player, pieces, last_move):
        """
        Checks whether the game has ended.

        :param mx: board's state.
        :param player: the one expected to play.
        :param pieces: player's pieces.
        :param last_move: the last move played.
        """

        global playable
        global castling_chance
        global in_check

        possible_draw = True

        if player == "White":
            player_castling = [True if x != 0 else False for x in castling_chance][:2]
        else:
            player_castling = [True if x != 0 else False for x in castling_chance][2:]

        in_check= is_attacked(mx, player, tuple(pieces), last_move, False)
        if in_check:
            print(paddings.BIG_PAD + colors.BOLD + "Check!" + colors.RESET)

        valid_moves = generator.possible_matrix(mx, player, tuple(pieces), last_move, tuple(player_castling))[1]

        if len(valid_moves) == 0 and in_check:
            
            # In case the player has no moves left
            # and remains in 'check', declare checkmate.
            # Otherwise, it will be declared stalemate.

            print(paddings.BIG_PAD + colors.BOLD + "Checkmate!" + colors.RESET)
            playable = 0

        if len(valid_moves) == 0 and not in_check:
            print(paddings.BIG_PAD + colors.BOLD + "Stalemate!" + colors.RESET)
            playable = 0

        for i in mx:
            if i != "-":
                if i.upper() not in "K":
                    possible_draw = 0
        
        if possible_draw:
            playable = 0
            print("It's a Tie!")

    
    def help_me(self):
        """
        A call for help, that explains the
        basic knowledge needed for someone to play.
        """

        os.system('cls' if os.name == 'nt' else 'clear') # nt is for Windows, otherwise Linux or Mac

        print("\n\n\n\n" + paddings.CENTER_PAD + "Hey! Let's play Chess! What's your move?\n\n" + colors.RESET + paddings.MIN_PAD +
        "Use algebraic notation to tell us that! For example, writing 'e2e3'\n" + paddings.MIN_PAD + 
        "would move your pawn from e2 to e3. To quit write the word " + colors.BOLD + "'stop'" + colors.RESET, "\n" + paddings.MIN_PAD +
        "and to reset the game, just write " +  colors.BOLD + "'restart'" + colors.RESET + ".\n" + paddings.MIN_PAD +
        "Type " + colors.BOLD + "'castleL'" + colors.RESET + " or " + colors.BOLD + "'castleR'" + colors.RESET +
        " in case you want to make that play\n" + paddings.MIN_PAD + "Take a look at the board and do your best!\n") 

        input(paddings.CENTER_PAD + "Understood? Type " + colors.BOLD + "anything" + colors.RESET + " to resume the game!\n\n" + paddings.BIG_PAD)
        
        board.output_matrix(self, mx, self.player1) 
        
    def gameplay(self):
        """
        Runs the game.
        """

        global mx
        global playable
        global moves_log
        global castling_chance
        global opening_state

        round = 0

        # Flags that assist the conversion
        # of the notation utilized to declare a given move
        # (SAN to Coordinate, in this particular program).


        flags = {"capture_flag": False, "check_flag": False, "ambiguous_flag": False}

        board.output_matrix(self, mx, "White")

        while playable:

            try:
                if round == 0 and self.player1 == "Black":
                    temp_mx = mx

                    # Storing the current game's state
                    # before the AI's turn.

                    print(colors.BOLD + "\n" +  paddings.MID_PAD + "┏━━━━━━━━━━━━━━━━━━\n" +  colors.BLINKING + paddings.BIG_PAD + "Hawkins' move... " + colors.RESET)

                    fen_state = generator.fen_generator(mx, self.player2)

                    # 'fen_state' will be needed in order
                    # to convert the move that will be extracted
                    # from gamelists.py's database to Coordinate Notation.

                    possible_lines = [line for line in game_moves]
                        
                    if len(possible_lines) != 0:
                            
                        # Pick a move from gamelists.py's database,
                        # limited to the games that are exactly the same
                        # to the one being played up until this point.

                        choice = random.randrange(0, len(possible_lines))
                        ai_response = possible_lines[choice][0]
                        san_moves_log.append(ai_response)
                        move = generator.change_notation(fen_state, ai_response)
                            
                        pos = list(move)
                        initial_pos = (8-int(pos[1]), movements.alge(pos[0])-1)
                        final = (8-int(pos[3]), movements.alge(pos[2])-1)
                            
                        result = check_order(mx, initial_pos, final, self.player1, moves_log[-1])
                            
                        if result[1] == "en_passant":
                            mx = generator.move(initial_pos, final, self.player1, "en_passant", mx, "letter")
                        else:
                            mx = generator.move(initial_pos, final, self.player1, "step", mx, "letter")

                    board.output_matrix(self, mx, self.player1)
                    moves_log.append(board.get_move(mx, temp_mx))

                    board.flags_reset(flags)
                    round += 1


                player_castling = [True if x != 0 else False for x in castling_chance]
                human_move = input(colors.BOLD + "\n" + paddings.MID_PAD + "┏━━━━━━━━━━━━━━━━━━\n" + paddings.BIG_PAD +"Make your move: ")
                
                while human_move == '':
                    board.output_matrix(self, mx, self.player1)
                    human_move = input(colors.BOLD + "\n" + paddings.MID_PAD + "┏━━━━━━━━━━━━━━━━━━\n" + paddings.BIG_PAD +"Make your move: ")
                
                if human_move.upper() in "STOP":
                    break

                if human_move.upper() in "RESTART":
                    playable = False
                    board.endgame(self)

                elif human_move.upper() in "HELP":

                    board.help_me(self)
                    continue

                elif human_move.upper() in "CASTLEL":
                    valid_moves = generator.possible_matrix( mx, self.player1, tuple(self.player1pieces), moves_log[-1], tuple(player_castling[:2]))[1]
                    if human_move in valid_moves:
                        mx = generator.castle(mx, self.player1, "left")
                        moves_log.append("O-O")
                    else:
                        board.output_matrix(self, mx, self.player1)
                        print(colors.BOLD + "\n"+ paddings.MID_PAD + "Illegal move, chief!")
                        continue
                elif human_move.upper() in "CASTLER":
                    valid_moves = generator.possible_matrix(mx, self.player1, tuple(self.player1pieces), moves_log[-1], tuple(player_castling[:2]))[1]
                    if human_move in valid_moves:
                        mx = generator.castle(mx, self.player1, "right")
                        moves_log.append("O-O-O")
                    else:
                        board.output_matrix(self, mx, self.player1)
                        print(colors.BOLD + "\n" + paddings.MID_PAD + "Illegal move, chief!")
                        continue
                else:
                    
                    # Taking an string and transforming
                    # it into coordinates on the board.

                    pos = list(human_move)
                    initial_pos = (8-int(pos[1]), movements.alge(pos[0])-1)
                    final = (8-int(pos[3]), movements.alge(pos[2])-1)
                    
                    result = check_order(mx, initial_pos, final, self.player1, moves_log[-1])
                    valid_moves = generator.possible_matrix(mx, self.player1, tuple(self.player1pieces), moves_log[-1], tuple(player_castling))[1]
                    
                    if human_move not in valid_moves or initial_pos == final or mx[final[0]*8 + final[1]] in self.player1pieces:
                        
                        board.output_matrix(self, mx, self.player1)
                        print(colors.BOLD + "\n" + paddings.MID_PAD + "Illegal move, chief!")
                        continue

                    if mx[initial_pos[0]*8 + initial_pos[1]].upper() in "P":
                        piece_moved = "P"

                    else:
                        piece_moved = mx[initial_pos[0]*8 + initial_pos[1]]
                        possible_pieces = [move for move in valid_moves if move[2:] == human_move[2:]]

                        for move in possible_pieces:
                            move_starting_point = list(move)
                            pos_start = (8-int(move_starting_point[1]), movements.alge(move_starting_point[0])-1)
                            if pos_start != initial_pos and mx[pos_start[0]*8 + pos_start[1]] == piece_moved:
                                
                                # In case theres a similar piece other than the one we moved
                                # that can also capture or move to the position that the chose,
                                # there's ambiguity in a way that we must specify which one
                                # of those pieces was actually played.
                                
                                flags["ambiguous_flag"] = True


                    if is_attacked(mx, self.player2, tuple(self.player2pieces), moves_log[-1], False):
                        flags["check_flag"] = True

                    if result[1] == "en_passant":
                        mx = generator.move(initial_pos, final, self.player1, "en_passant", mx, "letter")
                        flags["capture_flag"] = True

                    elif result[1] == "promotion":

                        # In case of promotion, leave the user
                        # with the option of choosing a Queen
                        # or a minor piece to replace his pawn. 

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
                
                # Check if the player has castled, or moved
                # any other pieces that stop him from doing so
                # in future moves.

                if True in player_castling[:2]:
                    if mx[7*8 + 4] != "K":
                        castling_chance[:2] =  [0,0]
                    else:
                        if player_castling[0] == True and mx[7*8] != "R":
                            castling_chance[0] = 0
                        if player_castling[1] == True and mx[7*8 + 7]!= "R":
                            castling_chance[1] = 0

                board.final(mx, self.player2, tuple(self.player2pieces), moves_log[-1])
                board.output_matrix(self, mx, self.player2)

                if playable == False:
                    board.endgame(self)

                else:
                    temp_mx = mx

                    # Storing the current game's state
                    # before the AI's turn.

                    print(colors.BOLD + "\n" +  paddings.MID_PAD + "┏━━━━━━━━━━━━━━━━━━\n" +  colors.BLINKING + paddings.BIG_PAD + "Hawkins' move... " + colors.RESET)
                    
                    if opening_state:

                        fen_state = generator.fen_generator(mx, self.player2)

                        # 'fen_state' will be needed in order
                        # to convert the move that will be extracted
                        # from gamelists.py's database to Coordinate Notation.

                        if self.player2 == "Black":
                            possible_lines = [line for line in game_moves if line[:round*2+1] == san_moves_log[1:]]
                        else:
                            possible_lines = [line for line in game_moves if line[:round*2] == san_moves_log[1:]]

                        if len(possible_lines) != 0:
                            
                            # Pick a move from gamelists.py's database,
                            # limited to the games that are exactly the same
                            # to the one being played up until this point.

                            choice = random.randrange(0, len(possible_lines))

                            if self.player2 == "Black":
                                ai_response = possible_lines[choice][1+round*2]
                            else:
                                ai_response = possible_lines[choice][round*2]

                            san_moves_log.append(ai_response)
                            move = generator.change_notation(fen_state, ai_response)
                            
                            pos = list(move)
                            initial_pos = (8-int(pos[1]), movements.alge(pos[0])-1)
                            final = (8-int(pos[3]), movements.alge(pos[2])-1)
                            
                            result = check_order(mx, initial_pos, final, self.player1, moves_log[-1])
                            
                            if result[1] == "en_passant":
                                mx = generator.move(initial_pos, final, self.player1, "en_passant", mx, "letter")
                            else:
                                mx = generator.move(initial_pos, final, self.player1, "step", mx, "letter")
                        else:

                            if self.depth == 1:
                                
                                # If the user selected the easiest level, ask Pluto
                                # (a weaker, Monte Carlo Tree Search AI) to play
                                # instead of Hawkins, who may be too strong.

                                mx = pluto.search(mx, self.player2, moves_log[-1], castling_chance)
                            else:
                                mx = hawkins.search(mx, self.player2, self.depth, moves_log[-1], castling_chance)
                            opening_state = False
                    else:

                        if self.depth == 1:
                            mx = pluto.search(mx, self.player2, moves_log[-1], castling_chance)
                        else:
                            mx = hawkins.search(mx, self.player2, self.depth, moves_log[-1], castling_chance)

                    
                    if True in player_castling[2:]:
                        if mx[4] != "k":
                            castling_chance[2:] =  [0,0]
                        else:
                            if player_castling[2] == True and mx[0] != "r":
                                castling_chance[3] = 0
                            if player_castling[3] == True and mx[7]!= "r":
                                castling_chance[3] = 0

                    board.output_matrix(self, mx, self.player1)
                    board.final(mx, self.player1, self.player1pieces, moves_log[-1])
                    board.endgame(self)
                    moves_log.append(board.get_move(mx, temp_mx))

                    if playable == False:
                        continue

                    board.flags_reset(flags)
                    round += 1

                    if round == 8:
                        opening_state = False
                    
            except:

                board.output_matrix(self, mx, self.player1)
                print(colors.BOLD + "\n" + paddings.MID_PAD + "That's not valid!")

                continue


colors = colors()
backgrounds = backgrounds()
paddings = paddings()
hawkins = Hawkins()
pluto = Pluto()

if __name__ == "__main__":

    os.system('cls' if os.name == 'nt' else 'clear') # nt is for Windows, otherwise Linux or Mac
    print(colors.BOLD + "\n\t HAWKINS\n" + colors.RESET + "━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("1 - Play the White Pieces\n2 - Play the Black Pieces\n3 - Game Difficulty\n")
    print("(To learn more about the commands\ntype 'help' once the game starts)\n")

    player = "NA"
    depth = 5
    choice = input("--> ")

    while choice not in ("1", "2"):

        if choice != "3":

            os.system('cls' if os.name == 'nt' else 'clear') # nt is for Windows, otherwise Linux or Mac
            print(colors.BOLD + "\n\t HAWKINS\n" + colors.RESET + "━━━━━━━━━━━━━━━━━━━━━━━━━")
            print("1 - Play the White Pieces\n2 - Play the Black Pieces\n3 - Game Difficulty")
            print("\nPlease select a valid option!\n")
            choice = input("--> ")

        while choice == "3":

            os.system('cls' if os.name == 'nt' else 'clear') # nt is for Windows, otherwise Linux or Mac
            print(colors.BOLD + "\n\t HAWKINS\n" + colors.RESET + "━━━━━━━━━━━━━━━━━━━━━━━━━")
            print("Press any key to exit the game difficulty menu\n\n1 - Apprentice (500 ELO)\n2 - Magician (1000 ELO)"
            "\n3 - Purple Sorcerer (1500 ELO)\n4 - Grand Mage (2000 ELO)\n\n")
            print("The AI's strength was estimated when facing\nStockfish, another open-source engine on lichess.org\n")
            difficulty = input("--> ")

            if difficulty == "1":
                depth = 1
            elif difficulty == "2":
                depth = 3
            elif difficulty == "3":
                depth = 4
            elif difficulty == "4":
                depth = 5

            os.system('cls' if os.name == 'nt' else 'clear') # nt is for Windows, otherwise Linux or Mac
            print(colors.BOLD + "\n\t HAWKINS\n" + colors.RESET + "━━━━━━━━━━━━━━━━━━━━━━━━━")
            print("1 - Play the White Pieces\n2 - Play the Black Pieces\n3 - Game Difficulty\n")
            choice = input("--> ")

    if choice == "1":
        player = "White"
    elif choice == "2":
        player = "Black"

    board(player, depth)

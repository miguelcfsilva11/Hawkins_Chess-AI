
from rules import is_attacked, check_order
from operator import itemgetter
from flask import Flask
from flask import request

app = Flask(__name__)


class generator:

    @staticmethod
    def turn_alge(number):
        """
        Takes a number, returns an alphabet letter
        corresponding to the column that it represents.
        """
        turn_alge_dic = {0: "a", 1:"b", 2:"c",
            3: "d", 4:"e", 5:"f", 6:"g", 7:"h"}
        return turn_alge_dic[number]
    

@app.route('/moves', methods=['POST'])
def possible_matrix():

    data = request.form
    mx = data["mx"]
    player = data["player"]
    pieces = tuple(data["pieces"].split(","))
    last_move = data["last_move"]
    castling_chance = tuple(data["castling_chance"].split(","))


    """
    Generates all possible moves and returns both an
    an array containing the board states and strings
    representing the legal plays in Coordinate Notation.

    :param mx: board's state.
    :param player: the color of player's pieces.
    :param last_move: the last move played.
    :param castling_chance: an array that holds
    information on whether each player can castle.
    """
    piece_value = {"P": 10, "Q": 90, "B": 30, "N": 30, "R": 50,
                    "p": 10, "q": 90, "b": 30, "n": 30, "r": 50, "k": 0, "K": 0}

    order_list = []
    final_options = []
    algebric_states = []
    if True in castling_chance:
        if player == "Black":
            king_side = 0
        else:
            king_side = 7
        if castling_chance[1] == True:
            if mx[king_side*8 + 5] == "-" and mx[king_side*8+6] == "-" and mx[king_side*8+4].upper() in "K" and mx[king_side*8+7].upper() in "R":
                if mx[king_side*8+4] in pieces and mx[king_side*8+7] in pieces and not is_attacked(mx, player, pieces, last_move, king_side*8+5):
                    if not is_attacked(mx, player, pieces, last_move, king_side*8+6) and not is_attacked(mx, player, pieces, last_move, king_side*8+4):
                        algebric_states.append("castleR")
                        value = 20
                        order_list.append((generator.castle(mx, player, "right"), value))

        if castling_chance[0] == True:
            if mx[king_side*8].upper() in "R" and mx[king_side*8+1] == "-" and mx[king_side*8+2] == "-" and mx[king_side*8+3] == "-" and mx[king_side*8+4].upper() in "K":
                if mx[king_side*8+4] in pieces and mx[king_side*8] in pieces and not is_attacked(mx, player, pieces, last_move, king_side*8+4):
                    
                    if not is_attacked(mx, player, pieces, last_move, king_side*8+2) and not is_attacked(mx, player, pieces, last_move, king_side*8+3):

                        algebric_states.append("castleL")
                        value = 20
                        order_list.append((generator.castle(mx, player, "left"), 20))
    
    for i in range(len(mx)):
        
        row = i//8
        col = i%8

        if mx[i].upper() in "P" and mx[i] in pieces:
            if player == "Black":
                if row+1 < 8: final_options.append((row+1,col))
                if row+2 < 8: final_options.append((row+2,col))
                if row+1 < 8 and col+1 < 8: final_options.append((row+1,col+1))
                if row+1 < 8 and col-1 > -1: final_options.append((row+1,col-1))
            else:
                if row-1 > -1: final_options.append((row-1,col))
                if row-2 > -1: final_options.append((row-2,col))
                if row-1 > -1 and col+1 < 8: final_options.append((row-1,col+1))
                if row-1 > -1 and col-1 > -1: final_options.append((row-1,col-1))

        if mx[i].upper() in "B" and mx[i] in pieces:
            current = (row,col)
            while current[0] > 0 and current[1] < 7:
                if mx[(current[0]-1)*8 + current[1]+1] != "-":
                    if mx[(current[0]-1)*8 + current[1]+1] not in pieces:
                        current= (current[0]-1, current[1]+1)
                        final_options.append(current)
                        break
                    break
                current= (current[0]-1, current[1]+1)
                final_options.append(current)
            current = (row,col)
            while current[0] > 0 and current[1] > 0:
                if mx[(current[0]-1)*8 + current[1]-1] != "-":
                    if mx[(current[0]-1)*8 + current[1]-1] not in pieces:
                        current= (current[0]-1, current[1]-1)
                        final_options.append(current)
                        break
                    break
                current= (current[0]-1, current[1]-1)
                final_options.append(current)
            current = (row,col)
            while current[0] < 7 and current[1] < 7:
                if mx[(current[0]+1)*8 + current[1]+1] != "-":
                    if mx[(current[0]+1)*8 + current[1]+1] not in pieces:
                        current= (current[0]+1, current[1]+1)
                        final_options.append(current)
                        break
                    break
                current= (current[0]+1, current[1]+1)
                final_options.append(current)
            current = (row,col)
            while current[0] < 7 and current[1] > 0:
                if mx[(current[0]+1)*8 + current[1]-1] != "-":
                    if mx[(current[0]+1)*8 + current[1]-1] not in pieces:
                        current= (current[0]+1, current[1]-1)
                        final_options.append(current)
                        break
                    break
                current= (current[0]+1, current[1]-1)
                final_options.append(current)
        if mx[i].upper() in "R" and mx[i] in pieces:
            current = (row,col)
            while current[0] > 0:
                if mx[(current[0]-1)*8 + current[1]] != "-":
                    if mx[(current[0]-1)*8 + current[1]] not in pieces:
                        current= (current[0]-1, current[1])
                        final_options.append(current)
                        break
                    break
                current= (current[0]-1, current[1])
                final_options.append(current)
            current = (row,col)
            while current[1] > 0:
                if mx[(current[0])*8 + current[1]-1] != "-":
                    if mx[(current[0])*8 + current[1]-1] not in pieces:
                        current= (current[0], current[1]-1)
                        final_options.append(current)
                        break
                    break
                current= (current[0], current[1]-1)
                final_options.append(current)
            current = (row,col)
            while current[0] < 7:
                if mx[(current[0]+1)*8 + current[1]] != "-":
                    if mx[(current[0]+1)*8 + current[1]] not in pieces:
                        current= (current[0]+1, current[1])
                        final_options.append(current)
                        break
                    break
                current= (current[0]+1, current[1])
                final_options.append(current)
            current = (row,col)
            while current[1] < 7:
                if mx[(current[0])*8 + current[1]+1] != "-":
                    if mx[(current[0])*8 + current[1]+1] not in pieces:
                        current= (current[0], current[1]+1)
                        final_options.append(current)
                        break
                    break
                current= (current[0], current[1]+1)
                final_options.append(current)
        if mx[i].upper() in "Q" and mx[i] in pieces:
            current = (row,col)
            while current[0] > 0 and current[1] < 7:
                if mx[(current[0]-1)*8 + current[1]+1] != "-":
                    if mx[(current[0]-1)*8 + current[1]+1] not in pieces:
                        current= (current[0]-1, current[1]+1)
                        final_options.append(current)
                        break
                    break
                current= (current[0]-1, current[1]+1)
                final_options.append(current)
            current = (row,col)
            while current[0] > 0 and current[1] > 0:
                if mx[(current[0]-1)*8 + current[1]-1] != "-":
                    if mx[(current[0]-1)*8 + current[1]-1] not in pieces:
                        current= (current[0]-1, current[1]-1)
                        final_options.append(current)
                        break
                    break
                current= (current[0]-1, current[1]-1)
                final_options.append(current)
            current = (row,col)
            while current[0] < 7 and current[1] < 7:
                if mx[(current[0]+1)*8 + current[1]+1] != "-":
                    if mx[(current[0]+1)*8 + current[1]+1] not in pieces:
                        current= (current[0]+1, current[1]+1)
                        final_options.append(current)
                        break
                    break
                current= (current[0]+1, current[1]+1)
                final_options.append(current)    
            current = (row,col)
            while current[0] <7 and current[1] > 0:
                if mx[(current[0]+1)*8 + current[1]-1] != "-":
                    if mx[(current[0]+1)*8 + current[1]-1] not in pieces:
                        current= (current[0]+1, current[1]-1)
                        final_options.append(current)
                        break
                    break
                current= (current[0]+1, current[1]-1)
                final_options.append(current)
            current = (row,col)
            while current[0] > 0:
                if mx[(current[0]-1)*8 + current[1]] != "-":
                    if mx[(current[0]-1)*8 + current[1]] not in pieces:
                        current= (current[0]-1, current[1])
                        final_options.append(current)
                        break
                    break
                current= (current[0]-1, current[1])
                final_options.append(current)
            current = (row,col)
            while current[1] > 0:
                if mx[(current[0])*8 + current[1]-1] != "-":
                    if mx[(current[0])*8 + current[1]-1] not in pieces:
                        current= (current[0], current[1]-1)
                        final_options.append(current)
                        break
                    break
                current= (current[0], current[1]-1)
                final_options.append(current)
            current = (row,col)
            while current[0] < 7:
                if mx[(current[0]+1)*8 + current[1]] != "-":
                    if mx[(current[0]+1)*8 + current[1]] not in pieces:
                        current= (current[0]+1, current[1])
                        final_options.append(current)
                        break
                    break
                current= (current[0]+1, current[1])
                final_options.append(current)
            current = (row,col)
            while current[1] < 7:
                if mx[(current[0])*8 + current[1]+1] != "-":
                    if mx[(current[0])*8 + current[1]+1] not in pieces:
                        current= (current[0], current[1]+1)
                        final_options.append(current)
                        break
                    break
                current = (current[0], current[1]+1)
                final_options.append(current) 
            current = (row,col)

        if mx[i].upper() in "K" and mx[i] in pieces:

            if row+1 < 8 and col+1 < 8: final_options.append((row+1, col+1))
            if row+1 <8: final_options.append((row+1, col))
            if row+1 <8 and col-1 > -1: final_options.append((row+1, col-1)) 
            if row-1 > -1 and col+1 < 8: final_options.append((row-1, col+1))
            if row-1 > -1: final_options.append((row-1, col))
            if row-1 > -1 and col-1 > -1: final_options.append((row-1, col-1))
            if col+1 <8: final_options.append((row, col+1))
            if col-1 > -1: final_options.append((row, col-1))

        if mx[i].upper() in "N" and mx[i] in pieces:

            if row+1 < 8 and col+ 2 < 8: final_options.append((row+1, col+2))
            if row+1 < 8 and col -2 > -1: final_options.append((row+1, col-2))
            if row+2 < 8 and col-1 > -1: final_options.append((row+2, col-1)) 
            if row+2 < 8 and col+1 < 8: final_options.append((row+2, col+1))
            if row-1 > -1 and col+2 < 8: final_options.append((row-1, col+2))
            if row-1 > -1 and col-2 > -1: final_options.append((row-1, col-2))
            if row-2 > -1 and col+1 < 8 :final_options.append((row-2, col+1))
            if row-2 > -1 and col-1 > -1 :final_options.append((row-2, col-1))

        for position in final_options:
            
            option = str(mx[:])
            result = check_order(mx, (row,col), position, player, last_move)
            attacked = is_attacked(mx, player, pieces, last_move, False)

            if result[1] == "promotion":
                if result[0] and (row,col) != position and mx[position[0]*8 + position[1]] not in pieces:
                    for letter in "QRKB":
                        possible = generator.move((row,col), position, player, result[1], option, letter)
                        attacked = is_attacked(possible, player, pieces, last_move, False)
                        if not attacked:
                            value = 90
                            order_list.append((possible, value))
                            alge_order = generator.turn_alge(col) + str(8-row) +  generator.turn_alge(position[1]) + str(8-position[0])
                            algebric_states.append(alge_order)

            else:
                if result[0] and (row,col) != position and mx[position[0]*8 + position[1]] not in pieces:
                    possible = generator.move((row,col), position, player, result[1], option, "letter")
                    attacked = is_attacked(possible, player, pieces, last_move, False)
                    if not attacked:
                        if mx[position[0]*8+ position[1]] not in pieces and mx[position[0]*8 + position[1]] != "-":
                            value =  piece_value[mx[position[0]*8 + position[1]]]
                            order_list.append((possible, value))
                        else:
                            value = 0
                            order_list.append((possible, value))
                        alge_order = generator.turn_alge(col) + str(8-row) +  generator.turn_alge(position[1]) + str(8-position[0])
                        algebric_states.append(alge_order)
    algebric_moves = []
    for string in algebric_states:
        if string not in algebric_moves:
            algebric_moves.append(string)

    dic_return = {"possible_moves": algebric_moves}

    return dic_return

@app.route('/moves', methods=['POST'])
def move():
    """
    Returns an updated board based
    on the move that was played.

    :param pos: moved piece's initial position.
    :param final: moved piece's final position.
    :param player: the color of the player's pieces.
    :param order: one of three possible move categories.
    :param mx: board's state.

    :param letter: in case of promotion, this parameter
    specifies to which piece the user desires to promote.
    """

    data = request.form
    mx = data["mx"]
    last_move = data["last_move"]
    letter = data["letter"]
    player = data["player"]
    pos = list(data["pos"].split(","))
    final = list(data["final"].split(","))

    if mx[pos[0]*8+ pos[1]].upper() in "K" and (pos[1] == final[1] - 2):
        return castle(mx, player, "right")

    if mx[pos[0]*8+ pos[1]].upper() in "K" and (pos[1] == final[1] + 3):
        return castle(mx, player, "left")

    order = check_order(mx, pos, final, player, last_move)


    mx = list(mx)

    if order == "en_passant":
        mx[final[0]*8 + final[1]] = mx[pos[0]*8 + pos[1]]
        mx[pos[0]*8+ pos[1]] = "-"
        mx[pos[0]*8 + final[1]] = "-"
    elif order == "promotion":
        if player == "White":
            mx[final[0]*8 + final[1]] = letter.upper()
        elif player == "Black":
            mx[final[0]*8 + final[1]] = letter.lower()
        mx[pos[0]*8 + pos[1]] = "-"
    else:
        mx[final[0]*8 + final[1]] = mx[pos[0]*8 + pos[1]]
        mx[pos[0]*8 + pos[1]] = "-"
    mx = "".join(mx)
    
    return mx


def castle(mx, player, side):
    """
    Updates the board after the
    selected castle move.

    :param player: the color of player's pieces.
    :param side: the left or right side of the board.
    """

    data = request.form
    mx = data["mx"]
    side = data["side"]
    player = data["player"]

    new_mx = list(mx)
    if player == "White":
        if side == "right":
            new_mx[7*8 + 4] = "-"
            new_mx[7*8 + 5] = "R"
            new_mx[7*8 + 6] = "K"
            new_mx[7*8 + 7] = "-"
        if side == "left":
            new_mx[7*8 + 0] = "-"
            new_mx[7*8 + 1] = "-"
            new_mx[7*8 + 2] = "K"
            new_mx[7*8 + 3] = "R"
            new_mx[7*8 + 4] = "-"
    if player == "Black":
        if side == "right":
            new_mx[4] = "-"
            new_mx[5] = "r"
            new_mx[6] = "k"
            new_mx[7] = "-"
        if side == "left":
            new_mx[0] = "-"
            new_mx[1] = "-"
            new_mx[2] = "k"
            new_mx[3] = "r"
            new_mx[4] = "-"
    kx = "".join(new_mx)
    return kx
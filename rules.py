from movements import *

class rules:

    def check_order(self, mx, pos, final, player, last_move):
        if mx[pos[0]*8 + pos[1]].upper() in "P": #if pawn
            return movements.pawn_movement(mx,pos, final, last_move, player)
        if mx[pos[0]*8 + pos[1]].upper() in "B": #if bishop
            return movements.bishop_movement(mx, pos, final, 8)
        if mx[pos[0]* 8 + pos[1]].upper() in "R": #if rook
            return movements.rook_movement(mx, pos, final, 8)
        if mx[pos[0]*8 + pos[1]].upper() in "N":
            return movements.knight_movement(mx, pos, final)
        if mx[pos[0]*8 + pos[1]].upper() in "K":
            if movements.rook_movement(mx, pos, final, 1)[0]:
                return movements.rook_movement(mx, pos, final, 1)
            if movements.bishop_movement(mx, pos, final, 1)[0]:
                return movements.bishop_movement(mx, pos, final, 1)
        if mx[pos[0]*8 + pos[1]].upper() in "Q":
            if movements.rook_movement(mx, pos, final, 8)[0]:
                return movements.rook_movement(mx, pos, final, 8)
            if movements.bishop_movement(mx, pos, final, 8)[0]:
                return movements.bishop_movement(mx, pos, final, 8)
        return (False, "nothing")


    def is_checkmate (self, mx, player):
        if player == "White":
            for i in mx:
                if i == "k":
                    return False
            return True
        for i in mx:
            if i == "K":
                return False
        return True

    def is_check(self, mx, player, last_move):
        for matrix in generator.possible_matrix(mx, player, white_pieces, last_move):
            king_found = False
            for letter in matrix:
                if (letter == "k" and player == "White") or (letter = "K" and player == "Black"):
                    king_found = True
            if king_found == False:
                return True

movements = movements()


#todo change 'final' functions to first chech is_check, if true, checkmate
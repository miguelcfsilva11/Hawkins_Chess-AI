from movements import *
from functools import lru_cache

def check_order(mx, pos, final, player, last_move):
    """
    Checks whether the piece that was played made a legal move
    given the board's state, the piece's initial position, final
    position, the last move played and the color of the player's pieces.

    :returns: a tuple that contains a boolean value
    and an string that categorizes the move.
    """
    if mx[pos[0]*8 + pos[1]].upper() in "P":
        return movements.pawn_movement(mx,pos, final, last_move, player)

    if mx[pos[0]*8 + pos[1]].upper() in "B":
        return movements.bishop_movement(mx, pos, final, 8)

    if mx[pos[0]* 8 + pos[1]].upper() in "R":
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


@lru_cache(maxsize = 200000)
def is_attacked(mx, player, pieces, last_move, step):
    """
    Checks if the selected square is under attack
    by atleast one of the opponent's pieces.

    :param mx: board's state.
    :param player: the color of player's pieces.
    :param pieces: a set that contains player's pieces.
    :param last_move: the last move played.
    
    :param step: coordinates of the selected square. 
    If this parameter is set to False, then the square
    that we must evaluate is the current position of
    the player's king.
    """

    for i in range(len(mx)):
        if mx[i].upper() in "K" and mx[i] in pieces:
            row = i//8
            col = i%8
            break
    if step:
        row = step//8
        col = step%8

    current = (row, col)

    if player == "White":
        if row-1 > -1 and col + 1 < 8 and mx[(row-1)*8 + col+1].upper() in "P" and mx[(row-1)*8 + col+1] not in pieces: return True
        if row-1 > -1 and col - 1 > -1 and mx[(row-1)*8 + col-1].upper() in "P" and mx[(row-1)*8 + col-1] not in pieces: return True
    else:
        if row+1 < 8 and col + 1 < 8 and mx[(row+1)*8 + col+1].upper() in "P" and mx[(row+1)*8 + col+1] not in pieces: return True
        if row+1 < 8 and col - 1 > -1 and mx[(row+1)*8 + col-1].upper() in "P" and mx[(row+1)*8 + col-1] not in pieces: return True
        
    # Knight's threat

    if row+1 < 8 and col+ 2 < 8 and mx[(row+1)*8 + col+2].upper() in "N" and mx[(row+1)*8 + col+2] not in pieces: return True
    if row+1 < 8 and col- 2 > -1 and mx[(row+1)*8 + col-2].upper() in "N" and mx[(row+1)*8 + col-2] not in pieces: return True
    if row+2 < 8 and col-1 > -1 and mx[(row+2)*8 + col-1].upper() in "N" and mx[(row+2)*8 + col-1] not in pieces: return True
    if row+2 < 8 and col+1 < 8 and mx[(row+2)*8 + col+1].upper() in "N" and mx[(row+2)*8 + col+1] not in pieces: return True
    if row-1 > -1 and col+2 < 8 and mx[(row-1)*8 + col+2].upper() in "N" and mx[(row-1)*8 + col+2] not in pieces: return True
    if row-1 > -1 and col-2 > -1 and mx[(row-1)*8 + col-2].upper() in "N" and mx[(row-1)*8 + col-2] not in pieces: return True
    if row-2 > -1 and col+1 < 8 and mx[(row-2)*8 + col+1].upper() in "N" and mx[(row-2)*8 + col+1] not in pieces: return True
    if row-2 > -1 and col-1 > -1 and mx[(row-2)*8 + col-1].upper() in "N" and mx[(row-2)*8 + col-1] not in pieces: return True

    # King's threat
        
    if row+1 < 8 and col+1 < 8 and mx[(row+1)*8 + col+1].upper() in "K" and mx[(row+1)*8 + col+1] not in pieces: return True
    if row+1 <8 and mx[(row+1)*8 + col].upper() in "K" and mx[(row+1)*8 + col] not in pieces: return True
    if row+1 <8 and col-1 > -1 and mx[(row+1)*8 + col-1].upper() in "K" and mx[(row+1)*8 + col-1] not in pieces: return True 
    if row-1 > -1 and col+1 < 8 and mx[(row-1)*8 + col+1].upper() in "K" and mx[(row-1)*8 + col+1] not in pieces: return True
    if row-1 > -1 and mx[(row-1)*8 + col].upper() in "K" and mx[(row-1)*8 + col] not in pieces: return True
    if row-1 > -1 and col-1 > -1 and mx[(row-1)*8 + col-1].upper() in "K" and mx[(row-1)*8 + col-1] not in pieces: return True
    if col+1 <8 and mx[(row)*8 + col+1].upper() in "K" and mx[(row)*8 + col+1] not in pieces: return True
    if col-1 > -1 and mx[(row)*8 + col-1].upper() in "K" and mx[(row)*8 + col-1] not in pieces: return True


    while current[0] < 7 and current[1] < 7:
        # Threat from first diagonal direction.
        if mx[(current[0]+1)*8 + current[1] + 1].upper() in "BQ" and mx[(current[0]+1)*8 + current[1] + 1] not in pieces:
            return True
        if mx[(current[0]+1)*8 + current[1] + 1] != "-":
            break
        current = (current[0]+1, current[1]+1)
        
    current = (row, col)
    while current[0] < 7 and current[1] > 0:
        # Threat from second diagonal direction.
        if mx[(current[0]+1)*8 + current[1] - 1].upper() in  "BQ" and mx[(current[0]+1)*8 + current[1] - 1] not in pieces:
            return True
        if mx[(current[0]+1)*8 + current[1] - 1] != "-":
            break
        current = (current[0]+1, current[1]-1)

    current = (row, col)
    while current[0] > 0 and current[1] < 7:
        # Threat from third diagonal direction.
        if mx[(current[0]-1)*8 + current[1] + 1].upper() in "BQ" and mx[(current[0]-1)*8 + current[1] + 1] not in pieces:
            return True
        if mx[(current[0]-1)*8 + current[1] + 1] != "-":
            break
        current = (current[0]-1, current[1]+1)

    current = (row, col)
    while current[0] > 0 and current[1] > 0:
        # Threat from forth diagonal direction.
        if mx[(current[0]-1)*8 + current[1]- 1].upper() in "BQ" and mx[(current[0]-1)*8 + current[1] - 1] not in pieces:
            return True
        if mx[(current[0]-1)*8 + current[1] - 1] != "-":
            break
        current = (current[0]-1, current[1]-1)

    current = (row, col)
    while current[0] < 7:
        # Threat from downwards.
        if mx[(current[0]+1)*8 + current[1]].upper() in "RQ" and mx[(current[0]+1)*8 + current[1]] not in pieces:
            return True
        if mx[(current[0]+1)*8 + current[1]] != "-":
            break
        current = (current[0]+1, current[1])

    current = (row, col)
    while current[1] > 0:
        # Threat from the left.
        if mx[(current[0])*8 + current[1] - 1].upper() in "RQ" and mx[(current[0])*8 + current[1]- 1] not in pieces:
            return True
        if mx[(current[0])*8 + current[1] - 1] != "-":
            break
        current = (current[0], current[1]-1)

    current = (row, col)
    while current[0] > 0:
        # Threat from upwards.
        if mx[(current[0]-1)*8 + current[1]].upper() in "RQ" and mx[(current[0]-1)*8 + current[1]] not in pieces:
            return True
        if mx[(current[0]-1)*8 + current[1]] != "-":
            break
        current = (current[0]-1, current[1])

    current = (row, col)
    while current[1] < 7:
        # Threat from the right.
        if mx[(current[0])*8 + current[1]+1].upper() in "RQ" and mx[(current[0])*8 + current[1] + 1] not in pieces:
            return True
        if mx[(current[0])*8 + current[1] + 1] != "-":
            break
        current = (current[0], current[1]+1)
    return False

movements = movements()


#this file will contain the eval function / heuristics needed to evaluate a each game state
# reenter values for returned score, as of now, it can surpass winning score
class points:
    def evaluate(self, mx):

        pawn_table =   [0,  0,  0,  0,  0,  0,  0,  0,
			            50, 50, 50, 50, 50, 50, 50, 50,
			            10, 10, 20, 30, 30, 20, 10, 10,
			            5,  5, 10, 25, 25, 10,  5,  5,
			            0,  0,  0, 20, 20,  0,  0,  0,
			            5, -5,-10,  0,  0,-10, -5,  5,
			            5, 10, 10,-20,-20, 10, 10,  5,
			            0,  0,  0,  0,  0,  0,  0,  0]

        knight_table = [-50,-40,-30,-30,-30,-30,-40,-50,
			            -40,-20,  0,  0,  0,  0,-20,-40,
			            -30,  0, 10, 15, 15, 10,  0,-30,
			            -30,  5, 15, 20, 20, 15,  5,-30,
			            -30,  0, 15, 20, 20, 15,  0,-30,
			            -30,  5, 10, 15, 15, 10,  5,-30,
			            -40,-20,  0,  5,  5,  0,-20,-40,
			            -50,-40,-30,-30,-30,-30,-40,-50]

        bishop_table = [-20,-10,-10,-10,-10,-10,-10,-20,
			            -10,  0,  0,  0,  0,  0,  0,-10,
			            -10,  0,  5, 10, 10,  5,  0,-10,
			            -10,  5,  5, 10, 10,  5,  5,-10,
			            -10,  0, 10, 10, 10, 10,  0,-10,
			            -10, 10, 10, 10, 10, 10, 10,-10,
			            -10,  5,  0,  0,  0,  0,  5,-10,
			            -20,-10,-10,-10,-10,-10,-10,-20]

        rook_table = [  0,  0,  0,  0,  0,  0,  0,  0,
			            5, 10, 10, 10, 10, 10, 10,  5,
			            -5,  0,  0,  0,  0,  0,  0, -5,
			            -5,  0,  0,  0,  0,  0,  0, -5,
			            -5,  0,  0,  0,  0,  0,  0, -5,
			            -5,  0,  0,  0,  0,  0,  0, -5,
			            -5,  0,  0,  0,  0,  0,  0, -5,
			             0,  0,  0,  5,  5,  0,  0,  0]

        queen_table = [ -20,-10,-10, -5, -5,-10,-10,-20,
			            -10,  0,  0,  0,  0,  0,  0,-10,
			            -10,  0,  5,  5,  5,  5,  0,-10,
			            -5,  0,  5,  5,  5,  5,  0, -5,
			             0,  0,  5,  5,  5,  5,  0, -5,
			            -10,  5,  5,  5,  5,  5,  0,-10,
			            -10,  0,  5,  0,  0,  0,  0,-10,
			            -20,-10,-10, -5, -5,-10,-10,-20]

        kingmid_table = [   -30,-40,-40,-50,-50,-40,-40,-30,
			                -30,-40,-40,-50,-50,-40,-40,-30,
			                -30,-40,-40,-50,-50,-40,-40,-30,
			                -30,-40,-40,-50,-50,-40,-40,-30,
			                -20,-30,-30,-40,-40,-30,-30,-20,
			                -10,-20,-20,-20,-20,-20,-20,-10,
			                20, 20,  0,  0,  0,  0, 20, 20,
			                20, 30, 10,  0,  0, 10, 30, 20]

        kingend_table = [   -50,-40,-30,-20,-20,-30,-40,-50,
			                -30,-20,-10,  0,  0,-10,-20,-30,
			                -30,-10, 20, 30, 30, 20,-10,-30,
			                -30,-10, 30, 40, 40, 30,-10,-30,
			                -30,-10, 30, 40, 40, 30,-10,-30,
			                -30,-10, 20, 30, 30, 20,-10,-30,
			                -30,-30,  0,  0,  0,  0,-30,-30,
			                -50,-30,-30,-30,-30,-30,-30,-50]

        piece_value = {"P": -10, "Q": -90, "B": -30, "N": -30, "R": -50,
                        "p": 10, "q": 90, "b": 30, "n": 30, "r": 50}

        piece_to_table = {"P": pawn_table, "Q": queen_table, "B": bishop_table, "N": knight_table, "R": rook_table,
                        "p": pawn_table[::-1], "q": queen_table[::-1], "b": bishop_table[::-1], "n": knight_table[::-1], "r": rook_table[::-1]}

        score = 0
        minor_pieces = 0
        for pos in range(len(mx)):
            if mx[pos] in "-":
                continue
            elif mx[pos] == "K":
                white_king_spot = pos
                continue
            elif mx[pos] == "k":
                black_king_spot = pos
                continue
            elif mx[pos].lower() == mx[pos] and mx[pos] != "p":
                minor_pieces += 1
            score += piece_value[mx[pos]]

            if mx[pos].lower() == mx[pos]:
                score -= (piece_to_table[mx[pos]][pos]/9)
            else:
                score += (piece_to_table[mx[pos]][pos]/9)
        if minor_pieces <= 2:
            score += (kingend_table[::-1][black_king_spot] - kingend_table[white_king_spot])/9
        else:
            score += (kingmid_table[::-1][black_king_spot] - kingmid_table[white_king_spot])/9

        return score
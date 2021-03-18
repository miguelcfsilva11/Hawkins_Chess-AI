# this file will contain the eval function / heuristics needed to evaluate a each game state
# reenter values for returned score, as of now, it can surpass winning score
import math

class points:
	def evaluate(self, mx):

		pawn_table = [  0,   0,   0,   0,   0,   0,   0,   0,
           				 75,  80,  85,  70, 100,  80,  85,  90,
            			 10,  30,  20,  45,  40,  30,  45,   10,
           				-20,  15,  -5,  15,  15,   0,  15, -15,
           				-25,   5,  10,   10,   5,   0,   0, -25,
           				-20,   10,   5, -10, -10,  0,   5, -20,
           				-30,   10,  -10, -35, -35, -15,   5, -30,
            			 0,   0,   0,   0,   0,   0,   0,   0]

		pawn_black_table = [  0,   0,   0,   0,   0,   0,   0,   0,
           				 75,  80,  85,  100, 70,  80,  85,  90,
            			 10,  30,  20,  40,  45,  30,  45,   10,
           				-20,  15,  -5,  15,  15,   0,  15, -15,
           				-25,   5,  10,   5,   10,   0,   0, -25,
           				-20,   10,   5, -10, -10,  0,   5, -20,
           				-30,   10,  -10, -35, -35, -15,   5, -30,
            			 0,   0,   0,   0,   0,   0,   0,   0]

		knight_table = [-65, -55, -75, -75, -10, -55, -60, -70,
            			-5,  -5, 100, -35,   5,  60,  -5, -15,
        				10,  70,   0,  75,  75,  30,  60,  -5,
            			25,  25,  45,  35,  35,  40,  25,  15,
            			0,   5,  30,  20,  25,  35,   5,   0,
           				-20,  10,  15,  20,  20,  15,  10, -15,
           				-25, -15,  5,   0,   5,   0, -25, -20,
           				-75, -25, -25, -25, -20, -35, -20, -70]
						   
		knight_black_table = [-65, -55, -75, -10, -75, -55, -60, -70,
            			-5,  -5, 100, 5,   -35,  60,  -5, -15,
        				10,  70,   0,  75,  75,  30,  60,  -5,
            			25,  25,  45,  35,  35,  40,  25,  15,
            			0,   5,  30,  25,  20,  35,   5,   0,
           				-20,  10,  15,  20,  20,  15,  10, -15,
           				-25, -15,  5,   5,   0,   0, -25, -20,
           				-75, -25, -25, -20, -25, -35, -20, -70]

		bishop_table = [-60, -80, -80, -75, -25,-110, -40, -50,
           				-10,  20,  35, -40, -40,  30,   0, -20,
            			-10,  40, -35,  40,  50, -10,  30, -15,
            			25,  20,  20,  35,  25,  25,  15,  10,
            			15,  10,  15,  25,  20,  15,   0,   5,
            			15,  25,  25,  15,   10,  25,  20,  15,
            			20,  20,  10,   5,   5,   5,  20,  15,
            			-10,   0, -15, -10, -15, -15, -10, -10]


		bishop_black_table = [-60, -80, -80, -25, -75,-110, -40, -50,
           				-10,  20,  35, -40, -40,  30,   0, -20,
            			-10,  40, -35,  50,  40, -10,  30, -15,
            			25,  20,  20,  25,  35,  25,  15,  10,
            			15,  10,  15,  20,  25,  15,   0,   5,
            			15,  25,  25,  10,   15,  25,  20,  15,
            			20,  20,  10,   5,   5,   5,  20,  15,
            			-10,   0, -15, -15, -10, -15, -10, -10]


		rook_table = [35,  30,  35,   5,  35,  35,  55,  50,
            			55,  30,  55,  65,  55,  60,  35,  60,
            			20,  35,  30,  35,  45,  25,  25,  15,
             			0,   5,  15,  15,  20,  -5,  -10,  -5,
           				-30, -35, -15, -20, -15, -30, -45, -30,
           				-40, -30, -40, -25, -25, -35, -25, -45,
           				-55, -40, -30, -25, -30, -45, -45, -55,
           				-30, -25, -20,   5,  0, -20, -30, -30]

		rook_black_table = [35,  30,  35,   35,  55,  35,  55,  50,
            			55,  30,  55,  55,  65,  60,  35,  60,
            			20,  35,  30,  45,  35,  25,  25,  15,
             			0,   5,  15,  20,  15,  -5,  -10,  -5,
           				-30, -35, -15, -15, -20, -30, -45, -30,
           				-40, -30, -40, -25, -25, -35, -25, -45,
           				-55, -40, -30, -30, -25, -45, -45, -55,
           				-30, -25, -20,   0,  5, -20, -30, -30]

		queen_table = [5,   0,  -10,-105,  70,  25,  85,  25,
            			15,  30,  50, -10,  20,  75,  55,  25,
            			-5,  45,  30,  60,  70,  65,  45,   0,
             			0, -15,  25,  15,  25,  20, -15,  -5,
           				-15, -15,  -5,  -5,  0, -10, -20, -20,
           				-30,  -5, -15, -10, -15, -15, -15, -25,
           				-35, -20,   0, -20, -15, -15, -20, -40,
           				-40, -30, -30, -15, -30, -35, -35, -40]

		queen_black_table = [5,   0,  -105,-10,  70,  25,  85,  25,
            			15,  30,  50, 20,  -10,  75,  55,  25,
            			-5,  45,  30,  70,  60,  65,  45,   0,
             			0, -15,  25,  25,  15,  20, -15,  -5,
           				-15, -15,  -5,  0,  -5, -10, -20, -20,
           				-30,  -5, -15, -15, -10, -15, -15, -25,
           				-35, -20,   0, -15, -20, -15, -20, -40,
           				-40, -30, -30, -30, -15, -35, -35, -40]

		kingmid_table = [5,  55,  45, -100, -100,  60,  85, -60,
           				-30,  10,  55,  55,  55,  55,  10,   5,
           				-60,  10, -55,  45, -70,  30,  35, -30,
           				-55,  50,  10,  -5, -20,  15,   0, -50,
           				-55, -45, -50, -30, -50, -50,  -10, -50,
           				-45, -45, -45, -80, -65, -30, -30, -30,
            			-5,   5, -15, -50, -60, -20,  10,   5,
            			20,  30,  -5, -15,   5,  0,  40,  20]

		kingmid_black_table = [5,  55,  45, -100, -100,  60,  85, -60,
           				-30,  10,  55,  55,  55,  55,  10,   5,
           				-60,  10, -55,  -70, 45,  30,  35, -30,
           				-55,  50,  10,  -20, -5,  15,   0, -50,
           				-55, -45, -50, -50, -30, -50,  -10, -50,
           				-45, -45, -45, -65, -85, -30, -30, -30,
            			-5,   5, -15, -60, -50, -20,  10,   5,
            			20,  30,  -5, 5,   -15,  0,  40,  20]
		

		kingend_table = [-50, -40, -30, -20, -20, -30, -40, -50,
						 -30, -20, -10,  0,  0, -10, -20, -30,
						 -30, -10, 20, 30, 30, 20, -10, -30,
						 -30, -10, 30, 40, 40, 30, -10, -30,
						 -30, -10, 30, 40, 40, 30, -10, -30,
						 -30, -10, 20, 30, 30, 20, -10, -30,
						 -30, -30,  0,  0,  0,  0, -30, -30,
						 -50, -30, -30, -30, -30, -30, -30, -50]

		piece_value = {"P": -100, "Q": -930, "B": -320, "N": -280, "R": -480,
					   "p": 100, "q": 930, "b": 320, "n": 280, "r": 480}
		piece_to_table = {"P": pawn_table, "Q": queen_table, "B": bishop_table, "N": knight_table, "R": rook_table,
						  "p": pawn_black_table[::-1], "q": queen_black_table[::-1], "b": bishop_black_table[::-1],
						  "n": knight_black_table[::-1], "r": rook_black_table[::-1]}

		minor_white_pieces = 0
		minor_black_pieces = 0
		white_bishops = 0
		black_bishops = 0
		queen_dif = 0
		score = 0

		for pos in range(len(mx)):
			if mx[pos] in "-":
				continue
			
			elif mx[pos] == "Q":
				queen_dif -= 1
			elif mx[pos] == "q":
				queen_dif += 1
			elif mx[pos] == "K":
				white_king_spot = pos
				continue
			elif mx[pos] == "k":
				black_king_spot = pos
				continue
			elif mx[pos].lower() == mx[pos] and mx[pos] != "p":
				minor_black_pieces += 1

				if mx[pos] == "b":
					black_bishops += 1
				if mx[pos] == "r":
					row = pos // 8
					col = pos % 8
					current =  (row, col)
					while current[0] < 7:
						if mx[(current[0]+1)*8 + current[1]] != "p":
							score += 5
						else:
							break
						current = (current[0]+1, current[1])

			elif mx[pos].upper() == mx[pos] and mx[pos] != "P":
				minor_white_pieces += 1

				if mx[pos] == "B":
					white_bishops += 1
				if mx[pos] == "R":

					row = pos // 8
					col = pos % 8
					current =  (row, col)
					while current[0] > 0:
						if mx[(current[0]-1)*8 + current[1]] != "P":
							score -= 5
						else:
							break
						current = (current[0]-1, current[1])

			score += piece_value[mx[pos]]
			if mx[pos].lower() == mx[pos]:
				score += piece_to_table[mx[pos]][pos]
			else:
				score -= piece_to_table[mx[pos]][pos]

		if minor_black_pieces <= 2 or minor_white_pieces <= 2: 
			score += (kingend_table[::-1][black_king_spot] - kingend_table[white_king_spot])
			score += math.sqrt(abs(4 - white_king_spot//8)^2 + abs(4 - white_king_spot%8)^2)
			score += (10 - math.sqrt(abs(black_king_spot//8 - white_king_spot//8)^2 + abs(black_king_spot%8 - white_king_spot%8)^2))
		else:
			score += (kingmid_black_table[::-1][black_king_spot] - kingmid_table[white_king_spot])

		if white_bishops == 2:
			score -= 40
		if black_bishops == 2:
			score += 40
		score += queen_dif * 200
		
		return score



"""
points = points()
print(points.evaluate("rnbqkbnrpppppppp-------------------------------PPPPPPP-RNBQKBNR"))
"""
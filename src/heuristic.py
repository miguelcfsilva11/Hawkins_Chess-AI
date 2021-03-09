#this file will contain the eval function / heuristics needed to evaluate a each game state
# reenter values for returned score, as of now, it can surpass winning score
class points:
	def evaluate(self,mx):
		piece_value = {"P": -10, "Q": -90, "B": -30, "N": -30, "R": -50, "p": 10, "q": 90, "b": 30, "n": 30, "r": 50}
		score = 0
		for pos in mx:
			if pos.upper() in "-K":
				continue
			score += piece_value[pos]
		return score
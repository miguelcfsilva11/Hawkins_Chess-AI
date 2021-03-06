#this file will contain the eval function / heuristics needed to evaluate a each game state
# reenter values for returned score, as of now, it can surpass winning score
class points:
    def evaluate(self, mx):
        piece_value = {"P": -1, "Q": -9, "B": -3, "N": -3, "R": -5,
                        "p": 1, "q": 9, "b": 3, "n": 3, "r": 5}
        pawn_table = ""
        score = 0
        for pos in mx:
            if pos.upper() in "K-":
                continue
            score += piece_value[pos]
            
        return score*10
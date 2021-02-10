class rules:

    def __init__(self):
        self.castling = True
    def alge(self, letter):
    
        alge_dic = {"a": 1, "b": 2,
        "c": 3, "d": 4,
        "e": 5, "f": 6,
        "g": 7, "h": 8}

        return alge_dic[letter]
    def check_movement(self, mx, pos, final, player, last_move):
        if player == "White":
            print(pos)
            print(final)
            if mx[pos[0]][pos[1]] == "P": #if pawn
                if pos[0]-1 == final[0] and pos[1] == final[1]:
                    if mx[final[0]][final[1]] == "-": #checking if there's space
                        if final[0] == 0:
                            return (True, "promotion")
                        return (True, "step")  #moving pawn one space
                if pos[0]-2 == final[0] and pos[1] == final[1]:
                    if pos[0] == 6 and final[0] == 4: #checking if the pawn is in its initial place
                        if mx[final[0]][final[1]] == "-" and mx[final[0]+1][final[1]] == "-": 
                            return (True, "step")  #moving pawn two space

                if pos[0]-1 == final[0] and pos[1] == final[1]-1:
                    if mx[final[0]][final[1]] != "-": #checking if there's a piece there to be eaten
                        return (True, "step")  #capturing piece
                    else:
                        if mx[pos[0]][pos[1]+1] == "p": #checking en passant
                            if pos[0] == 3:
                                pawn_pos = list(last_move)
                                if 8-int(pawn_pos[3]) == 3 and 8-int(pawn_pos[1]) == 1 and rules.alge(self, pawn_pos[0])-1 == pos[1]+1:
                                    return (True, "en_passant")   

                if pos[0]-1 == final[0] and pos[1] == final[1]+1:
                    if mx[final[0]][final[1]] != "-":
                        return (True, "step")
                    else:
                        if mx[pos[0]][pos[1]-1] == "p": # checking en passant
                            if pos[0] == 3:
                                pawn_pos = list(last_move)
                                print(pawn_pos)
                                print(rules.alge(self, pawn_pos[0]))
                                print(pos[1]-1)
                                if 8-int(pawn_pos[3]) == 3 and 8-int(pawn_pos[1]) == 1 and rules.alge(self, pawn_pos[0])-1 == pos[1]-1:
                                    return (True, "en_passant") 
            if mx[pos[0]][pos[1]] == "B": #if bishop
                current = pos
                print("bishop found")
                for _ in range(8): #max diagonal length
                    current = (current[0]-1, current[1]+1)
                    if 0 > current[0] or current[0] > 7 or 0 > current[1] or current[1] > 7:
                        break
                    if current == final:
                        return (True, "step")
                    if mx[current[0]][current[1]] != "-":
                        break
                current = pos # reseting position
                for _ in range(8): #max diagonal length
                    current = (current[0]-1, current[1]-1)
                    if 0 > current[0] or current[0] > 7 or 0 > current[1] or current[1] > 7:
                        break
                    if current == final:
                        return (True, "step")
                    if mx[current[0]][current[1]] != "-":
                        break
                current = pos # reseting position
                for _ in range(8): #max diagonal length
                    current = (current[0]+1, current[1]-1)
                    if 0 > current[0] or current[0] > 7 or 0 > current[1] or current[1] > 7:
                        break
                    if current == final:
                        return (True, "step")
                    if mx[current[0]][current[1]] != "-":
                        break
                current = pos # reseting position
                for _ in range(8): #max diagonal length
                    current = (current[0]+1, current[1]+1)
                    if 0 > current[0] or current[0] > 7 or 0 > current[1] or current[1] > 7:
                        break
                    if current == final:
                        return (True, "step")
                    if mx[current[0]][current[1]] != "-":
                        break
            if mx[pos[0]][pos[1]] == "R": #if rook
                current = pos
                print("rook found")
                for _ in range(8): #max row/collumn length
                    current = (current[0]-1, current[1])
                    if 0 > current[0] or current[0] > 7 or 0 > current[1] or current[1] > 7:
                        break
                    if current == final:
                        return (True, "step")
                    if mx[current[0]][current[1]] != "-":
                        break
                current = pos
                for _ in range(8):
                    current = (current[0]+1, current[1])
                    if 0 > current[0] or current[0] > 7 or 0 > current[1] or current[1] > 7:
                        break
                    if current == final:
                        return (True, "step")
                    if mx[current[0]][current[1]] != "-":
                        break
                current = pos
                for _ in range(8):
                    current = (current[0], current[1]-1)
                    if 0 > current[0] or current[0] > 7 or 0 > current[1] or current[1] > 7:
                        break
                    if current == final:
                        return (True, "step")
                    if mx[current[0]][current[1]] != "-":
                        break
                current = pos
                for _ in range(8): 
                    current = (current[0], current[1]+1)
                    if 0 > current[0] or current[0] > 7 or 0 > current[1] or current[1] > 7:
                        break
                    if current == final:
                        return (True, "step")
                    if mx[current[0]][current[1]] != "-":
                        break
            print("nonono")
            return (False, "nothing")
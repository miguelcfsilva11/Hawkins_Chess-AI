class movements:

    @staticmethod
    def alge(letter):
        
        alge_dic = {"a": 1, "b": 2,
        "c": 3, "d": 4,
        "e": 5, "f": 6,
        "g": 7, "h": 8}

        return alge_dic[letter]
    
    def pawn_movement(self,mx, pos, final, last_move, player):
        
        if player == "White":
            if pos[0]-1 == final[0] and pos[1] == final[1]:
                if mx[final[0]*8 + final[1]] == "-": #checking if there's space
                    if final[0] == 0:
                        return (True, "promotion")
                    return (True, "step")  #moving pawn one space
            if pos[0]-2 == final[0] and pos[1] == final[1]:
                #print("this is it!")
                if pos[0] == 6 and final[0] == 4: #checking if the pawn is in its initial place
                    if mx[final[0]*8 + final[1]] == "-" and mx[(final[0]+1)*8 + final[1]] == "-": 
                        return (True, "step")  #moving pawn two space

            if pos[0]-1 == final[0] and pos[1] == final[1]-1:
                if mx[final[0]*8 + final[1]] != "-": #checking if there's a piece there to be eaten
                    if final[0] == 0:
                        return (True, "promotion")
                    return (True, "step")  #capturing piece
                else:
                    if mx[pos[0]*8 + pos[1]+1] == "p": #checking en passant
                        if pos[0] == 3:
                            pawn_pos = list(last_move)
                            if last_move != "O-O-O" and last_move != "O-O" and 8-int(pawn_pos[3]) == 3 and 8-int(pawn_pos[1]) == 1 and movements.alge(pawn_pos[0])-1 == pos[1]+1:
                                return (True, "en_passant")  
            if pos[0]-1 == final[0] and pos[1] == final[1]+1:
                if mx[final[0]*8 + final[1]] != "-":
                    if final[0] == 0:
                        return (True, "promotion")
                    return (True, "step")
                else:
                    if mx[pos[0]*8 + pos[1]-1] == "p": # checking en passant
                        if pos[0] == 3:
                            pawn_pos = list(last_move)
                            if last_move != "O-O-O" and last_move != "O-O" and 8-int(pawn_pos[3]) == 3 and 8-int(pawn_pos[1]) == 1 and movements.alge(pawn_pos[0])-1 == pos[1]-1:
                                return (True, "en_passant")
            return (False, "nothing")

        else:

            if pos[0]+1 == final[0] and pos[1] == final[1]:
                if mx[final[0]*8 + final[1]] == "-": #checking if there's space
                    if final[0] == 7:
                        return (True, "promotion")
                    return (True, "step")  #moving pawn one space
            if pos[0]+2 == final[0] and pos[1] == final[1]:
                if pos[0] == 1 and final[0] == 3: #checking if the pawn is in its initial place
                    if mx[final[0]*8 + final[1]] == "-" and mx[(final[0]-1) * 8 + final[1]] == "-": 
                        return (True, "step")  #moving pawn two space

            if pos[0]+1 == final[0] and pos[1] == final[1]-1:
                if mx[final[0]*8 + final[1]] != "-": #checking if there's a piece there to be eaten
                    if final[0] == 7:
                        return (True, "promotion")
                    return (True, "step")  #capturing piece
                else:
                    if mx[pos[0]*8 + pos[1]+1] == "p": #checking en passant
                        if pos[0] == 4:
                            pawn_pos = list(last_move)
                            if last_move != "O-O-O" and last_move != "O-O" and 8-int(pawn_pos[3]) == 4 and 8-int(pawn_pos[1]) == 6 and movements.alge(pawn_pos[0])-1 == pos[1]+1:
                                return (True, "en_passant")  
            if pos[0]+1 == final[0] and pos[1] == final[1]+1:
                if mx[final[0]*8 + final[1]] != "-":
                    if final[0] == 7:
                        return (True, "promotion")
                    return (True, "step")
                else:
                    if mx[pos[0]*8 + pos[1]-1] == "p": # checking en passant
                        if pos[0] == 4:
                            pawn_pos = list(last_move)
                            if last_move != "O-O-O" and last_move != "O-O" and 8-int(pawn_pos[3]) == 4 and 8-int(pawn_pos[1]) == 6 and movements.alge(pawn_pos[0])-1 == pos[1]-1:
                                return (True, "en_passant")
            return (False, "nothing")

    def bishop_movement(self, mx, pos, final, steps):
        current = pos
        for _ in range(steps): #max diagonal length
            current = (current[0]-1, current[1]+1)
            if 0 > current[0] or current[0] > 7 or 0 > current[1] or current[1] > 7:
                break
            if current == final:
                return (True, "step")
            if mx[current[0]*8 + current[1]] != "-":
                break
        current = pos
        for _ in range(steps):
            current = (current[0]-1, current[1]-1)
            if 0 > current[0] or current[0] > 7 or 0 > current[1] or current[1] > 7:
                break
            if current == final:
                return (True, "step")
            if mx[current[0]*8 + current[1]] != "-":
                break
        current = pos
        for _ in range(steps):
            current = (current[0]+1, current[1]-1)
            if 0 > current[0] or current[0] > 7 or 0 > current[1] or current[1] > 7:
                break
            if current == final:
                return (True, "step")
            if mx[current[0]*8 + current[1]] != "-":
                break
        current = pos
        for _ in range(steps):
            current = (current[0]+1, current[1]+1)
            if 0 > current[0] or current[0] > 7 or 0 > current[1] or current[1] > 7:
                break
            if current == final:
                return (True, "step")
            if mx[current[0]*8 +current[1]] != "-":
                break
        return (False, "nothing")

    def rook_movement(self, mx, pos, final, steps):
        current = pos
        for _ in range(steps): #max row/collumn length
            current = (current[0]-1, current[1])
            if 0 > current[0] or current[0] > 7 or 0 > current[1] or current[1] > 7:
                break
            if current == final:
                return (True, "step")
            if mx[current[0]*8 + current[1]] != "-":
                break
        current = pos
        for _ in range(steps):
            current = (current[0]+1, current[1])
            if 0 > current[0] or current[0] > 7 or 0 > current[1] or current[1] > 7:
                break
            if current == final:
                return (True, "step")
            if mx[current[0]*8 + current[1]] != "-":
                break
        current = pos
        for _ in range(steps):
            current = (current[0], current[1]-1)
            if 0 > current[0] or current[0] > 7 or 0 > current[1] or current[1] > 7:
                break
            if current == final:
                return (True, "step")
            if mx[current[0]*8 + current[1]] != "-":
                break
        current = pos
        for _ in range(steps): 
            current = (current[0], current[1]+1)
            if 0 > current[0] or current[0] > 7 or 0 > current[1] or current[1] > 7:
                break
            if current == final:
                return (True, "step")
            if mx[current[0]*8 + current[1]] != "-":
                break
        return (False, "nothing")

    def knight_movement(self, mx, pos, final):
        if pos[0]-2 == final[0] and pos[1]+1 == final[1]:
            return (True, "step")
        if pos[0]-2 == final[0] and pos[1]-1 == final[1]:
            return (True, "step")
        if pos[0]+2 == final[0] and pos[1]+1 == final[1]:
            return (True, "step")
        if pos[0]+2 == final[0] and pos[1]-1 == final[1]:
            return (True, "step")
        if pos[0]-1 == final[0] and pos[1]+2 == final[1]:
            return (True, "step")
        if pos[0]-1 == final[0] and pos[1]-2 == final[1]:
            return (True, "step")
        if pos[0]+1 == final[0] and pos[1]+2 == final[1]:
            return (True, "step")
        if pos[0]+1 == final[0] and pos[1]-2 == final[1]:
            return (True, "step")
        return (False, "nothing")
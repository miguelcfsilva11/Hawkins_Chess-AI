from rules import*
from copy import deepcopy
class generator:
    def possible_matrix(self, mx, player, pieces, last_move):
        possible_states = [] #generate child_nodes
        final_options = []
        for i in range(len(mx)):
            for k in range(len(mx[i])):
                if mx[i][k].upper() in "P" and mx[i][k] in pieces:
                    if i+1 < 8: final_options.append((i+1,k))
                    if i+2 < 8: final_options.append((i+2,k))
                    if i+1 < 8 and k+1 <8: final_options.append((i+1,k+1))
                    if i+1 < 8 and k-1 > -1: final_options.append((i+1,k-1))
                if mx[i][k].upper() in "B" and mx[i][k] in pieces:
                    current = (i,k)
                    while current[0] > 0 and current[1] < 7:
                        current= (current[0]-1, current[1]+1)
                        final_options.append(current)
                    current = (i,k)
                    while current[0] > 0 and current[1] > 0:
                        current= (current[0]-1, current[1]-1)
                        final_options.append(current)
                    current = (i,k)
                    while current[0] < 7 and current[1] < 7:
                        current= (current[0]+1, current[1]+1)
                        final_options.append(current)
                    current = (i,k)
                    while current[0] < 7 and current[1] > 0:
                        current= (current[0]+1, current[1]-1)
                        final_options.append(current)
                if mx[i][k].upper() in "R" and mx[i][k] in pieces:
                    current = (i,k)
                    while current[0] > 0:
                        current= (current[0]-1, current[1])
                        final_options.append(current)
                    current = (i,k)
                    while current[1] > 0:
                        current= (current[0], current[1]-1)
                        final_options.append(current)
                    current = (i,k)
                    while current[0] < 7:
                        current= (current[0]+1, current[1])
                        final_options.append(current)
                    current = (i,k)
                    while current[1] < 7:
                        current= (current[0], current[1]+1)
                        final_options.append(current)
                if mx[i][k].upper() in "Q" and mx[i][k] in pieces:
                    current = (i,k)
                    while current[0] > 0 and current[1] < 7:
                        current= (current[0]-1, current[1]+1)
                        final_options.append(current)
                    current = (i,k)
                    while current[0] > 0 and current[1] > 0:
                        current= (current[0]-1, current[1]-1)
                        final_options.append(current)
                    current = (i,k)
                    while current[0] < 7 and current[1] < 7:
                        current= (current[0]+1, current[1]+1)
                        final_options.append(current)
                    current = (i,k)
                    while current[0] < 7 and current[1] > 0:
                        current= (current[0]+1, current[1]-1)
                        final_options.append(current)
                    current = (i,k)
                    while current[0] > 0:
                        current= (current[0]-1, current[1])
                        final_options.append(current)
                    current = (i,k)
                    while current[1] > 0:
                        current= (current[0], current[1]-1)
                        final_options.append(current)
                    current = (i,k)
                    while current[0] < 7:
                        current= (current[0]+1, current[1])
                        final_options.append(current)
                    current = (i,k)
                    while current[1] < 7:
                        current = (current[0], current[1]+1)
                        final_options.append(current) 
                if mx[i][k].upper() in "K" and mx[i][k] in pieces:
                    if i+1 < 8 and k+1 < 8: final_options.append((i+1, k+1))
                    if i+1 <8: final_options.append((i+1, k))
                    if i+1 <8 and k-1 > -1: final_options.append((i+1, k-1)) 
                    if i-1 > -1 and k+1 < 8: final_options.append((i-1, k+1))
                    if i-1 > -1: final_options.append((i-1, k))
                    if i-1 > -1 and k-1 > -1: final_options.append((i-1, k-1))
                    if k+1 <8: final_options.append((i, k+1))
                    if k-1 > -1: final_options.append((i, k-1))
                if mx[i][k].upper() in "N" and mx[i][k] in pieces:
                    if i+1 < 8 and k+ 2 < 8: final_options.append((i+1, k+2))
                    if i+1 < 8 and k -2 > -1: final_options.append((i+1, k-2))
                    if i+2 < 8 and k-1 > -1: final_options.append((i+2, k-1)) 
                    if i+2 < 8 and k+1 < 8: final_options.append((i+2, k+1))
                    if i-1 > -1 and k+2 < 8: final_options.append((i-1, k+2))
                    if i-1 > -1 and k-2 > -1: final_options.append((i-1, k-2))
                    if i-2 > -1 and k+1 < 8 :final_options.append((i-2, k+1))
                    if i-2 > -1 and k-1 > -1 :final_options.append((i-2, k-1))
                print(final_options)
                for position in final_options:
                    result = rules.check_order(mx, (i,k), position, player, last_move)
                    if result[0]:
                        print("found result")
                        possible_states.append(generator.move(self, (i,k), position, player, result[1], mx))
                final_options = []
        return possible_states

    def move(self, pos, final, player, order, mx):
        print(order)
        if order == "en_passant":
            print("order processed")
            mx[final[0]][final[1]] = mx[pos[0]][pos[1]]
            mx[pos[0]][pos[1]] = "-"
            mx[pos[0]][final[1]] = "-"
        elif order == "promotion":
            if player == "White":
                mx[final[0]][final[1]] = "Q"
            elif player == "Black":
                mx[final[0]][final[1]] = "q"
            mx[pos[0]][pos[1]] = "-"
        else:
            mx[final[0]][final[1]] = mx[pos[0]][pos[1]]
            mx[pos[0]][pos[1]] = "-"
        return mx

rules = rules()

#todo read everyscript again try to use idiomatic python and list comprehensions whenever i can
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
                for position in final_options:
                    option = deepcopy(mx)
                    result = rules.check_order(mx, (i,k), position, player, last_move)
                    if  result[0] and (i,k) != position and mx[position[0]][position[1]] not in pieces: possible_states.append(generator.move(self, (i,k), position, player, result[1], option))
                final_options = []
        #for mx in possible_states:
         #   printable_matrix = ("\t8 {0}\n\t7 {1}\n\t6 {2}\n"
          #                   "\t5 {3}\n\t4 {4}\n\t3 {5}\n "
           #                   "\t2 {6}\n\t1 {7}\n\t {8}\t{9}{10}{11}{12}{13}{14}{15}").format(mx[0], mx[1], mx[2], mx[3],
            #                                        mx[4], mx[5], mx[6], mx[7],"   a", " b", "    c","    d","    e","    f","    g","    h")
            #print("\n" + printable_matrix + "\n")
        return possible_states

    def move(self, pos, final, player, order, mx):
        if order == "en_passant":
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


mx=[["r","n","b","q","k","b","n","r"],
    ["p","p","p","p","p","p","p","p"],
    ["-","-","-","-","-","-","-","-"],
    ["-","-","-","-","-","-","-","-"],
    ["-","-","-","-","-","-","-","-"],
    ["-","-","-","-","-","-","-","-"],
    ["P","P","P","P","P","P","P","P"],
    ["R","N","B","Q","K","B","N","R"]]


#todo read everyscript again try to use idiomatic python and list comprehensions whenever i can
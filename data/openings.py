import re

# Feel free to expand this project by adding
# more games to the gamelists.py script

open('opening_var.txt','w').writelines([ line for line in open('modern_q.txt') if line[0:2] == "1."])
open('opening_var.txt','a').writelines([ line for line in open('nimzo.txt') if line[0:2] == "1."])
open('opening_var.txt','a').writelines([ line for line in open('carlsen.txt') if line[0:2] == "1."])
open('opening_var.txt','a').writelines([ line for line in open('nakamura.txt') if line[0:2] == "1."])
open('opening_var.txt','a').writelines([ line for line in open('karpov.txt') if line[0:2] == "1."])
open('opening_var.txt','a').writelines([ line for line in open('kasparov.txt') if line[0:2] == "1."])
open('opening_var.txt','a').writelines([ line for line in open('anand.txt') if line[0:2] == "1."])
open('opening_var.txt','a').writelines([ line for line in open('giri.txt') if line[0:2] == "1."])
open('opening_var.txt','a').writelines([ line for line in open('karjakin.txt') if line[0:2] == "1."])


f = open("opening_var.txt",'r')
lines = f.readlines()
f.close()

excluded_words = ["1", ".", "2", "3", "4", "5", "6", "7", "8","9"]

newLines = []

for line in lines:
    a = line.split(".")
    b = (" ").join(a)
    c = b.split(" ")

    newLines.append([word for word in c if word not in excluded_words])

f = open("opening_var.txt", 'w')
for line in newLines:
    f.write("{},\n".format(line))

f.close()

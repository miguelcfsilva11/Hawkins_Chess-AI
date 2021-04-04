import re

# Running this script will update the 'opening_var.txt' file.
# Copy the content stored in that file and paste it into the
# 'game_moves' variable on 'gamelists.py'. Feel free to expand
# this project by adding more games in '.txt' format to this script.
 
open('data\samples\opening_var.txt','w').writelines([ line for line in open('data\samples\modern_q.txt') if line[0:2] == "1."])
open('data\samples\opening_var.txt','a').writelines([ line for line in open('data\samples\nimzo.txt') if line[0:2] == "1."])
open('data\samples\opening_var.txt','a').writelines([ line for line in open('data\samples\data\openings\carlsen.txt') if line[0:2] == "1."])
open('data\samples\opening_var.txt','a').writelines([ line for line in open('data\samples\nakamura.txt') if line[0:2] == "1."])
open('data\samples\opening_var.txt','a').writelines([ line for line in open('data\samples\karpov.txt') if line[0:2] == "1."])
open('data\samples\opening_var.txt','a').writelines([ line for line in open('data\samples\kasparov.txt') if line[0:2] == "1."])
open('data\samples\opening_var.txt','a').writelines([ line for line in open('data\samples\anand.txt') if line[0:2] == "1."])
open('data\samples\opening_var.txt','a').writelines([ line for line in open('data\samples\giri.txt') if line[0:2] == "1."])
open('data\samples\opening_var.txt','a').writelines([ line for line in open('data\samples\karjakin.txt') if line[0:2] == "1."])

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

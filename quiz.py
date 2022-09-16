import random
import os

f = open("1.txt","r",encoding='utf-16')

questions = {}
functions = []
descriptions = []
for line in f.readlines():
    data = line.split("\t")
    questions[data[0].strip()] = data[1].strip()
    descriptions.append(data[1].strip())
    functions.append(data[0].strip())

q = random.choices(functions,k=10)
random.shuffle(descriptions)

score = 0

for f in range(len(q)):
    a = random.choices(descriptions,k=4)
    answer = questions[q[f]]
    a.append(answer)
    random.shuffle(a)
    print("Q %d/10 : What is the correct description of this function? \n" %(f+1))
    print(q[f])
    print()
    print(" 1. %s \n 2. %s \n 3. %s \n 4. %s \n 5. %s " %tuple(a))
    choice = input()
    print()
    if a[int(choice)-1] == answer:
        print("Correct")
        score += 1
    else:
        print("Wrong. answer is: %s" %answer)
    print()
    next = input("Press Enter for Next Question")
    os.system("cls")

print("You got %d/10 questions right" %score)
"""
Created on Fri Sep 17 14:33:36 2021

@author: Ankita Dasgupta
"""
import random
import numpy as np
import matplotlib.pyplot as plt 
import seaborn as sns
#from matplotlib import colors
from matplotlib import rcParams

# Labels
labelx = ["A","B","C","D","E"]
labely = ["5","4","3","2","1"]

opBoard = np.zeros((5,5))
#opBoard[1:6, 1] = 1 # Carrier 5
#opBoard[5:9, 8] = 1 # Battleship 4
opBoard[3, 1:3] = 1 # Submarine 3
opBoard[1:3, 2] = 1 # Destroyer 2

# Board with explored states
exploredBoard = np.zeros((5,5))

# Total 14 spaces on the board occupied 
def generateGraph(board, counter):
    #name = "plot" + str(counter)
    cmap = "seismic"
    ax1 = sns.heatmap(board, linewidth = 0.5, cmap = cmap, cbar=False)
    ax2 = sns.heatmap(opBoard, linewidth = 0.5, cmap = cmap, cbar=False)
    plt.legend([],[], frameon = False)
    ax1.set_xticklabels(labelx)
    ax1.set_yticklabels(labely)
    ax2.set_xticklabels(labelx)
    ax1.set_yticklabels(labely)
    rcParams['figure.figsize'] = 6,6
    plt.show()
    
# List of unexplored tiles
empty = []
for i in range(0,5):
    for j in range(0,5):
        empty.append(str(i)+str(j))
print(empty)

def randomGuess(opBoard, exploredBoard, counter, hit, empty):
    if hit >= 4:
        print("Number of Turns: ",counter)
        print("Sucessfull Hits: ",hit)
        generateGraph(exploredBoard, counter)
        return True
    random_n = random.choice(empty)
    empty.remove(random_n)
    row = int(random_n[0])
    col = int(random_n[1])
    generateGraph(exploredBoard, counter)
    if opBoard[row,col] == 1:
        hit = hit + 1
        exploredBoard[row,col] = 1
    else:
        exploredBoard[row,col] = 2
    randomGuess(opBoard, exploredBoard, counter+1, hit, empty)

randomGuess(opBoard, exploredBoard, 0, 0, empty)

print(empty)
#print(generateGraph(opBoard))
#print(opBoard)

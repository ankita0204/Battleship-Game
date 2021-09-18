"""
Created on Fri Sep 17 20:40:52 2021

@author: Ankita Dasgupta
"""
import random
import numpy as np
import matplotlib.pyplot as plt 
import seaborn as sns
#from matplotlib import colors
from matplotlib import rcParams
import gc 

# Labels
labelx = ["A","B","C","D","E","F","G","H","I","J"]
labely = ["10","9","8","7","6","5","4","3","2","1"]

opBoard = np.zeros((10,10))
opBoard[1:6, 1] = 1 # Carrier 5
opBoard[5:9, 8] = 1 # Battleship 4
opBoard[3, 4:7] = 1 # Submarine 3
opBoard[5, 4:7] = 1 # Submarine 3
opBoard[8, 4:6] = 1 # Destroyer 2

# Board with explored states
exploredBoard = np.zeros((10,10))
probBoard = np.zeros((10,10))

# Total 14 spaces on the board occupied 
def generateGraph(board, counter):
    #name = "plot" + str(counter)
    cmap = "seismic"
    ax = sns.heatmap(board, linewidth = 0.5, cmap = cmap, cbar=False)
    plt.legend([],[], frameon = False)
    ax.set_xticklabels(labelx)
    ax.set_yticklabels(labely)
    rcParams['figure.figsize'] = 11,11
    plt.show()
    
# List of unexplored tiles
empty = []
for i in range(0,10):
    for j in range(0,10):
        empty.append(str(i)+str(j))

def firstMove(empty):
    return (random.choice(empty))

def generateMove(probBoard):
    return (np.unravel_index(probBoard.argmax(), probBoard.shape))

def generate_probBoard(probBoard, last_hit):
    if last_hit[0]>=0 and last_hit[0]<=9 and last_hit[1]+1>=0 and last_hit[1]+1<=9:
        if probBoard[last_hit[0], last_hit[1]+1] == 0:
            probBoard[last_hit[0], last_hit[1]+1] += 0.25

    if last_hit[0]>=0 and last_hit[0]<=9 and last_hit[1]-1>=0 and last_hit[1]-1<=9:
        if probBoard[last_hit[0], last_hit[1]-1] == 0:
            probBoard[last_hit[0], last_hit[1]-1] += 0.25
    
    if last_hit[0]+1>=0 and last_hit[0]+1<=9 and last_hit[1]>=0 and last_hit[1]<=9:
        if probBoard[last_hit[0]+1, last_hit[1]] == 0:
            probBoard[last_hit[0]+1, last_hit[1]] += 0.25

    if last_hit[0]-1>0 and last_hit[0]<=9 and last_hit[1]-1>=0 and last_hit[1]<=9:
        if probBoard[last_hit[0]-1, last_hit[1]] == 0:
            probBoard[last_hit[0]-1, last_hit[1]] += 0.25
    return(probBoard)

def randomUsingProbability (opBoard, counter, hit, empty, probBoard, last_hit, missed, exploredBoard):
    if hit >= 17 or counter>=100:
        print("Number of Turns: ",counter)
        print("Sucessfull Hits: ",hit)
        generateGraph(exploredBoard, counter)
        #print(probBoard)
        return
    
    if (last_hit == -1): #last hit was miss && don't know have a place to check, so we take random guess
        print("random", counter)
        random_num = firstMove(empty)
        empty.remove(random_num)
        row = int(random_num[0])
        col = int(random_num[1])
        generateGraph(exploredBoard, counter)
        #print(probBoard)

        if opBoard[row,col] == 1:    
            hit += 1
            last_hit = [row,col]
            exploredBoard[row,col] = 1
            probBoard[row,col]=-10 # random hit
            exploredBoard[row,col]=1
            probBoard = generate_probBoard(probBoard, last_hit)
        else:
            probBoard[row,col]=-1 # miss
            exploredBoard[row,col]=2
    else:
        nextHit = generateMove(probBoard)
        position = str(nextHit[0])+str(nextHit[1])
        if position in empty:  # should always be true
            empty.remove(position)     
            row = nextHit[0]
            col = nextHit[1]
            generateGraph(exploredBoard, counter)
            #print(probBoard)
            
            if probBoard[row,col] == 0:  #out of guesses
                last_hit = -1
                
            probBoard[row,col]=-1
            if opBoard[row,col] == 1:    
                hit += 1
                last_hit = [row,col]
                exploredBoard[row,col] = 1
                probBoard[row,col]=-100 # rated move hit
                exploredBoard[row,col]=1
                missed = 0
            else:
                missed = 1
                exploredBoard[row,col]=2
    randomUsingProbability (opBoard, counter+1, hit, empty, probBoard, last_hit, missed, exploredBoard)
    
randomUsingProbability(opBoard, 0, 0, empty, probBoard, -1, 0, exploredBoard)
#print(probBoard)
#randomGuess(opBoard, exploredBoard, 0, 0, empty)
print(empty)
#print(generateGraph(opBoard))
#print(opBoard)
gc.collect()

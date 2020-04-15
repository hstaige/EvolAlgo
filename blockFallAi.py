import numpy as np
from pynput.keyboard import Key, Controller
import random

def aiLoop(weights,playerLoc,enemyList,screenWidth,screenHeight,playerWidth):
    #controls player movements while running game

    """
    Section 1.) Get relative y-position of enemies to left, above, and right
    """
    #scales values down to how many playerwidths they are

    yVals = [0,0,0]
    enemyTemp = [0,0]

    for [idx,position] in enumerate(yVals):
        for enemy in enemyList:
            enemyTemp[1] = enemy[1]/screenHeight #y vals in terms of amount up screen
            checkedValue = playerLoc[0]+(idx-1)*playerWidth
            if checkedValue == -playerWidth:
                checkedValue = screenWidth - playerWidth
            elif checkedValue == screenWidth:
                checkedValue = 0
            if enemy[0] == checkedValue:
                if enemyTemp[1] > position:
                    yVals[idx] = enemyTemp[1]

    """
    Section 2.) determines which direction to go based on current weights
    """
    yVals = np.array(yVals)
    output = np.dot(yVals,weights)

    maxidx = np.argmax(output)

    keyboard = Controller()

    if maxidx == 0 and output[0] != 0:
        return(0)
    elif maxidx == 1:
        return(1)
    elif maxidx == 2:
        return(2)


def fillWithRands(dim1,dim2=1):
    """
    Fills a np array [dim1,dim2] with random values between -1 and 1.

    INPUT: dim1 (int); Optionally dim2 (int)

    OUTPUT: random array [dim1, dim2]
    """
    temp = np.zeros((dim1,dim2))
    for i in range(dim1):
        for j in range(dim2):
            temp[i,j] = random.randint(-100,100)/100
    return temp

import pygame
import sys
import random
from blockFallAi import *

pygame.init()


#set constants for game; can be changed
WIDTH = 800
HEIGHT = 600
playerSize = 50

RED = (255,0,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
backgroundColor = (0,0,0)

enemySize = 50
enemyPos = [enemySize * random.randint(1,16),enemySize]
enemyList = [enemyPos]

playerPos = [int(WIDTH/2),int(HEIGHT-playerSize)]

screen = pygame.display.set_mode((WIDTH, HEIGHT))

clock = pygame.time.Clock()
gameOver = False
exitStart = False

speed = 10
score = 0
difficulty = 0

epochs = 100
speciesNumber = 10
jiggle = 5

titleFont = pygame.font.SysFont("monospace", 35)
subscriptFont = pygame.font.SysFont("monospace", 20)



#creates new enemies if there are less than 10
def dropEnemies(enemyList,score):
    delay = random.random()
    if len(enemyList) < 10 and delay < score/10:
        xPos = playerSize * random.randint(0,15)
        yPos = 0
        enemyList.append([xPos,yPos])

#draws enemies on screen, cycling through all
def drawHorizontalEnemies(enemyList):
    for enemyPos in enemyList:
        pygame.draw.rect(screen, BLUE, (int(enemyPos[0]), int(enemyPos[1]), \
                        enemySize, enemySize))

#changes the position of enemies, killing those below the screen
def updateEnemyPosition(enemyList, score):
    for idx, enemyPos in enumerate(enemyList):
        if enemyPos[1] >= 0 and enemyPos[1] <= HEIGHT:
            enemyPos[1] += speed
        else:
            enemyList.pop(idx)
            score = score + 1
    return score

#checks collision for all enemies
def collisionCheck(enemyList):
    for enemyPos in enemyList:
        if detectCollision(playerPos, enemyPos):
            return True
    return False

#checks collisions for one enemy, used in collisionCheck
def detectCollision(playerPos, enemyPos):
    pX = playerPos[0]
    pY = playerPos[1]

    eX = enemyPos[0]
    eY = enemyPos[1]

    if (eX >= pX and eX < (pX + playerSize)) or \
    (pX >= eX and pX < (eX + enemySize)):
        if (eY >= pY and eY < (pY + playerSize)) or \
        (pY >= eY and pY < (eY + enemySize)):
            return True
    return False

#launches on start up, allows for selection of difficulty
def intializeGame():
    difficulty = 0

    startText = "Select a difficulty!"
    label = titleFont.render(startText, 1, RED)
    screen.blit(label, (int(WIDTH-WIDTH*7/8), int(HEIGHT/2)))

    startText = "1 for Easy, 2 for Medium, 3 for a bAd TiMe"
    label = subscriptFont.render(startText, 1, BLUE)
    screen.blit(label, (int(WIDTH-WIDTH*7/8), int(HEIGHT/2+100)))


    pygame.display.update()

    while difficulty == 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    difficulty = .3
                    break
                if event.key == pygame.K_2:
                    difficulty = .6
                    break
                if event.key == pygame.K_3:
                    difficulty = .9
                    break

    return difficulty

#updates speed based on current score and difficulty
def setLevel(score,speed, difficulty):
    if score < 50:
        speed = (score/10 + 10)
    elif score < 200:
        speed = (score-50)/20 + 15
    else:
        speed = 22.5

    speed = speed * difficulty

    return speed



#Waits until difficulty is selected to startText
while difficulty == 0:
    difficulty = intializeGame()

if difficulty == .9:
    #INTIATESANSMODE
    pass
    #pygame.mixer.music.load("SANS.MP3")
    #pygame.mixer.music.play(33)

weightList = []

for species in range(speciesNumber):
    weightList.append(fillWithRands(3,3))


for epoch in range(epochs):

    scoreList = []

    #loops through all species
    for species in weightList:
        score = 0
        gameOver = False
        enemyPos = [enemySize * random.randint(1,16),enemySize]
        enemyList = [enemyPos]
        playerPos = [int(WIDTH/2),int(HEIGHT-playerSize)]
        #Game Loop
        while not gameOver:
            x = playerPos[0]
            y = playerPos[1]
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        y += playerSize
                    if event.key == pygame.K_UP:
                        y -= playerSize
                    if event.key == pygame.K_LEFT:
                        x -= playerSize
                    elif event.key == pygame.K_RIGHT:
                        x += playerSize
                #keeps player in play playspace

                playerPos = [x,y]


            screen.fill(backgroundColor)

            score = updateEnemyPosition(enemyList, score)
            speed = setLevel(score, speed, difficulty)

            text = "Score: " + str(score)
            label = titleFont.render(text, 1, YELLOW)
            screen.blit(label, (WIDTH-200, HEIGHT-40))

            if collisionCheck(enemyList) or score > 1000:
                gameOver = True
                enemyList = []


            direction = aiLoop(species,(x,y),enemyList,WIDTH,HEIGHT,playerSize)

            if direction == 0:
                x -= playerSize
            elif direction == 2:
                x += playerSize

            if x < 0:
                x = WIDTH - playerSize
            if x > (WIDTH - playerSize):
                x = 0
            if y < HEIGHT - 3 * playerSize:
                y = HEIGHT -3 * playerSize
            if y > HEIGHT - playerSize:
                y = HEIGHT - playerSize

            playerPos = [x,y]


            pygame.draw.rect(screen, RED, (playerPos[0], playerPos[1], playerSize, playerSize))
            drawHorizontalEnemies(enemyList)
            dropEnemies(enemyList, score)

            clock.tick(300)
            pygame.display.update()

        scoreList.append(score)

    print(scoreList)
    print(np.mean(scoreList))
    scoreList = np.array(scoreList)
    worst = np.argmin(scoreList)
    topScorerIdxs = []
    while len(topScorerIdxs) < 5:
        topScorerIdxs.append(np.argmax(scoreList))
        scoreList[topScorerIdxs[-1]] = 0

    tempWeightList = [0,0,0,0,0,0,0,0,0,0]

    # for [idx,topScorer] in enumerate(topScorerIdxs):
    #     tempWeightList[2*idx] = weightList[topScorer]
    #     tempWeightList[2*idx+1] = weightList[topScorer]

    temp = np.zeros((3,3))
    for i in range(len(weightList[topScorerIdxs[0]])):
        for j in range(len(weightList[topScorerIdxs[0]][i])):
            temp[i,j] = weightList[topScorerIdxs[0]][i][j]
    weightList[worst] = temp

    for i in range(len(weightList)):
        for j in range(len(weightList[i])):
            for k in range(len(weightList[i][j])):
                value = weightList[i][j][k]
                value = value + random.randint(-jiggle,jiggle)/100
                weightList[i][j][k] = value
    print(weightList)

print("Your final score was: ",score, "!!!")

if score > 150:
    print("... and you won! Good job!")

print(weightList)

import math
import copy

NUM_ROWS = 6
NUM_COLS = 7
DEFAULT_VAL = '_'
PLAYER_VAL = 'x'
AI_VAL = 'o'
START_DEPTH = 5

def initGrid():
    grid = []
    for i in range(NUM_ROWS):
        row = []
        for j in range(NUM_COLS):
            row.append(DEFAULT_VAL)
        grid.append(row)
    return grid

def printGrid(grid):
    for i in range(NUM_ROWS):
        row = ''
        for j in range(NUM_COLS):
            row += grid[i][j] + '  '
        print(row)

def getUserInput():
    userInput = input('Select column to drop piece: ')
    return int(userInput)-1

def dropPiece(player, grid, yIndex):
    for x in range(NUM_ROWS-1):
        if grid[x][yIndex] == DEFAULT_VAL and grid[x+1][yIndex] != DEFAULT_VAL:
            grid[x][yIndex] = player
            return
    grid[NUM_ROWS-1][yIndex] = player

def isWinningWindow(w, x, y, z):
    return w != DEFAULT_VAL and w == x and x == y and y == z

def findWinner(grid):
    # horizontal windows
    for x in range(NUM_ROWS):
        for y in range(0, NUM_COLS-3):
            if isWinningWindow(grid[x][y], grid[x][y+1], grid[x][y+2], grid[x][y+3]):
                return grid[x][y]
    # vertical windows
    for y in range(NUM_COLS):
        for x in range(NUM_ROWS-3):
            if isWinningWindow(grid[x][y], grid[x+1][y], grid[x+2][y], grid[x+3][y]):
                return grid[x][y]
    # positive gradient windows
    for x in range(3):
        tempX = x
        for y in range(3-x):
            if isWinningWindow(grid[tempX][y], grid[tempX+1][y+1], grid[tempX+2][y+2], grid[tempX+3][y+3]):
                return grid[tempX][y]
            tempX += 1
    for y in range(1, 4):
        tempY = y
        for x in range(4-y):
            if isWinningWindow(grid[x][tempY], grid[x+1][tempY+1], grid[x+2][tempY+2], grid[x+3][tempY+3]):
                return grid[x][tempY]
            tempY += 1
    # negative gradient windows
    for x in range(3):
        tempX = x
        for y in range(NUM_COLS-1, NUM_COLS-4+x, -1):
            if isWinningWindow(grid[tempX][y], grid[tempX+1][y-1], grid[tempX+2][y-2], grid[tempX+3][y-3]):
                return grid[tempX][y]
            tempX += 1
    for y in range(NUM_COLS-2, NUM_COLS-5, -1):
        tempY = y
        i = 0
        for x in range(3-i):
            if isWinningWindow(grid[x][tempY], grid[x+1][tempY-1], grid[x+2][tempY-2], grid[x+3][tempY-3]):
                return grid[x][tempY]
            tempY -= 1
        i += 1
    return None

def centerScore(grid):
    score = 0
    for x in range(NUM_ROWS):
        if grid[x][int(NUM_COLS/2)] == AI_VAL:
            score += 3
    return score

def windowScore(w, x, y, z):
    windowScore = 0
    window = [w, x, y, z]
    emptyCount = window.count(DEFAULT_VAL)
    aiCount = window.count(AI_VAL)
    playerCount = window.count(PLAYER_VAL)
    if aiCount == 4:
        windowScore += 1000
    elif aiCount == 3 and emptyCount == 1:
        windowScore += 5
    elif aiCount == 2 and emptyCount == 2:
        windowScore += 2
    if playerCount == 3 and emptyCount == 1:
        windowScore -= 4
    return windowScore

def horizontalScore(grid):
    horizScore = 0
    for x in range(NUM_ROWS):
        for y in range(NUM_COLS-3):
            horizScore += windowScore(grid[x][y], grid[x][y+1], grid[x][y+2], grid[x][y+3])
    return horizScore

def verticalScore(grid):
    vertScore = 0
    for y in range(NUM_COLS):
        for x in range(NUM_ROWS-3):
            vertScore += windowScore(grid[x][y], grid[x+1][y], grid[x+2][y], grid[x+3][y])
    return vertScore

def diagonalScore(grid):
    diagScore = 0
    # positive gradient
    for x in range(3):
        tempX = x
        for y in range(3-x):
            diagScore += windowScore(grid[tempX][y], grid[tempX+1][y+1], grid[tempX+2][y+2], grid[tempX+3][y+3])
            tempX += 1
    for y in range(1, 4):
        tempY = y
        for x in range(4-y):
            diagScore += windowScore(grid[x][tempY], grid[x+1][tempY+1], grid[x+2][tempY+2], grid[x+3][tempY+3])
            tempY += 1

    # negative gradient
    for x in range(3):
        tempX = x
        for y in range(NUM_COLS-1, NUM_COLS-4+x, -1):
            diagScore += windowScore(grid[tempX][y], grid[tempX+1][y-1], grid[tempX+2][y-2], grid[tempX+3][y-3])
            tempX += 1
    for y in range(NUM_COLS-2, NUM_COLS-5, -1):
        tempY = y
        i = 0
        for x in range(3-i):
            diagScore += windowScore(grid[x][tempY], grid[x+1][tempY-1], grid[x+2][tempY-2], grid[x+3][tempY-3])
            tempY -= 1
        i += 1
    return diagScore

def evalGrid(grid):
    score = 0
    score += centerScore(grid)
    score += horizontalScore(grid)
    score += verticalScore(grid)
    score += diagonalScore(grid)
    return score

def isValidMove(grid, yIndex):
    return grid[0][yIndex] == DEFAULT_VAL

def moveExplorationSequence():
    # explore from center column to edge columns 
    sequence = []
    mid = int(NUM_COLS/2)
    sequence.append(mid)
    for i in range(1, mid+1):
        sequence.append(mid+i)
        sequence.append(mid-i)
    return sequence

def miniMax(grid, depth, isMaximizing, alpha, beta):
    if depth == 0 or findWinner(grid) != None:
        return evalGrid(grid)
    if isMaximizing:
        maxEval = -math.inf
        selectedMove = None
        for y in moveExplorationSequence():
            if not isValidMove(grid, y): continue
            nextGrid = copy.deepcopy(grid)
            dropPiece(AI_VAL, nextGrid, y)
            eval = miniMax(nextGrid, depth-1, not isMaximizing, alpha, beta)
            if eval > maxEval:
                maxEval = eval
                selectedMove = y
            alpha = max(alpha, eval)
            if beta <= alpha: break
        if depth == START_DEPTH:
            return selectedMove
        else: return maxEval
    else:
        minEval = math.inf
        for y in moveExplorationSequence():
            if not isValidMove(grid, y): continue
            nextGrid = copy.deepcopy(grid)
            dropPiece(PLAYER_VAL, nextGrid, y)
            eval = miniMax(nextGrid, depth-1, not isMaximizing, alpha, beta)
            minEval = min(minEval, eval)
            beta = min(beta, eval)
            if beta <= alpha: break
        return minEval

def startGame():
    grid = initGrid()
    playerTurn = True
    while(findWinner(grid) == None):
        if playerTurn:
            printGrid(grid)
            selectedCol = getUserInput()
            if not isValidMove(grid, selectedCol): 
                print("Column is filled!")
                continue
            dropPiece(PLAYER_VAL, grid, selectedCol)
        else:
            dropPiece(AI_VAL, grid, miniMax(grid, START_DEPTH, True, -math.inf, math.inf))
        playerTurn = not playerTurn

startGame()

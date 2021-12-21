import math
import copy

NUM_ROWS = 6
NUM_COLS = 7
DEFAULT_VAL = '_'
PLAYER_ONE_VAL = 'x'
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
    for x in range(0, NUM_ROWS):
        for y in range(0, NUM_COLS-3):
            if isWinningWindow(grid[x][y], grid[x][y+1], grid[x][y+2], grid[x][y+3]):
                return grid[x][y]
    # vertical windows
    for y in range(0, NUM_COLS):
        for x in range(0, NUM_ROWS-3):
            if isWinningWindow(grid[x][y], grid[x+1][y], grid[x+2][y], grid[x+3][y]):
                return grid[x][y]
    # positive gradient windows
    for x in range(0, 3):
        for y in range(0, 3-x):
            if isWinningWindow(grid[x][y], grid[x+1][y+1], grid[x+2][y+2], grid[x+3][y+3]):
                return grid[x][y]
    for y in range(1, 4):
        for x in range(0, 4-x):
            if isWinningWindow(grid[x][y], grid[x+1][y+1], grid[x+2][y+2], grid[x+3][y+3]):
                return grid[x][y]
    # negative gradient windows
    for x in range(0, 3):
        for y in range(NUM_COLS-1, NUM_COLS-4, -1):
            if isWinningWindow(grid[x][y], grid[x+1][y-1], grid[x+2][y-2], grid[x+3][y-3]):
                return grid[x][y]
    for y in range(NUM_COLS-2, NUM_COLS-5, -1):
        for x in range(0, 3):
            if isWinningWindow(grid[x][y], grid[x+1][y-1], grid[x+2][y-2], grid[x+3][y-3]):
                return grid[x][y]
    return None

def centerScore(grid):
    score = 0
    for x in range(0, NUM_ROWS):
        if grid[x][int(NUM_COLS/2)] == AI_VAL:
            score += 3
    return score

def windowScore(w, x, y, z):
    windowScore = 0
    window = [w, x, y, z]
    emptyCount = window.count(DEFAULT_VAL)
    aiCount = window.count(AI_VAL)
    playerCount = window.count(PLAYER_ONE_VAL)
    if aiCount == 4:
        windowScore += 100
    elif aiCount == 3 and emptyCount == 1:
        windowScore += 5
    elif aiCount == 2 and emptyCount == 2:
        windowScore += 2
    if playerCount == 3 and emptyCount == 1:
        windowScore -= 4
    return windowScore

def horizontalScore(grid):
    horizScore = 0
    for x in range(0, NUM_ROWS):
        for y in range(0, NUM_COLS-3):
            horizScore += windowScore(grid[x][y], grid[x][y+1], grid[x][y+2], grid[x][y+3])
    return horizScore

def verticalScore(grid):
    vertScore = 0
    for y in range(0, NUM_COLS):
        for x in range(0, NUM_ROWS-3):
            vertScore += windowScore(grid[x][y], grid[x+1][y], grid[x+2][y], grid[x+3][y])
    return vertScore

def diagonalScore(grid):
    diagScore = 0
    # positive gradient
    for x in range(0, 3):
        for y in range(0, 3-x):
            diagScore += windowScore(grid[x][y], grid[x+1][y+1], grid[x+2][y+2], grid[x+3][y+3])
    for y in range(1, 4):
        for x in range(0, 4-x):
            diagScore += windowScore(grid[x][y], grid[x+1][y+1], grid[x+2][y+2], grid[x+3][y+3])

    # negative gradient
    for x in range(0, 3):
        for y in range(NUM_COLS-1, NUM_COLS-4, -1):
            diagScore += windowScore(grid[x][y], grid[x+1][y-1], grid[x+2][y-2], grid[x+3][y-3])
    for y in range(NUM_COLS-2, NUM_COLS-5, -1):
        for x in range(0, 3):
            diagScore += windowScore(grid[x][y], grid[x+1][y-1], grid[x+2][y-2], grid[x+3][y-3])
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

def miniMax(grid, depth, isMaximizing):
    if depth == 0 or findWinner(grid) != None:
        return evalGrid(grid)
    if isMaximizing:
        maxEval = -math.inf
        selectedMove = None
        for y in range(NUM_COLS):
            if not isValidMove(grid, y): continue
            nextGrid = copy.deepcopy(grid)
            dropPiece(AI_VAL, nextGrid, y)
            eval = miniMax(nextGrid, depth-1, not isMaximizing)
            if eval > maxEval:
                maxEval = eval
                selectedMove = y
        if depth == START_DEPTH:
            return selectedMove
        else: return maxEval
    else:
        minEval = math.inf
        for y in range(NUM_COLS):
            if not isValidMove(grid, y): continue
            nextGrid = copy.deepcopy(grid)
            dropPiece(PLAYER_ONE_VAL, nextGrid, y)
            eval = miniMax(nextGrid, depth-1, not isMaximizing)
            minEval = min(minEval, eval)
        return minEval

def startGame():
    grid = initGrid()
    playerTurn = True
    while(findWinner(grid) == None):
        if playerTurn:
            printGrid(grid)
            dropPiece(PLAYER_ONE_VAL, grid, getUserInput())
        else:
            dropPiece(AI_VAL, grid, miniMax(grid, START_DEPTH, True))
        playerTurn = not playerTurn

startGame()

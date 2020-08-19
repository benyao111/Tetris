
import math, copy, random

from cmu_112_graphics import *

def almostEqual(d1, d2, epsilon=10**-7):
    # note: use math.isclose() outside 15-112 with Python version 3.5 or later
    return (abs(d2 - d1) < epsilon)

import decimal
def roundHalfUp(d):
    rounding = decimal.ROUND_HALF_UP
    return int(decimal.Decimal(d).to_integral_value(rounding=rounding))

def timerFired(app):
    if app.isGameOver == False:
    #moveFallingPiece(app, 0, 0)
        if moveFallingPiece(app, 1, 0) == False:
            placeFallingPiece(app)
            newFallingPiece(app)
            removeFullRows(app)
            if fallingPieceIsLegal(app) == False:
                app.isGameOver = True
def gameDimensions():
    (rows, cols, cellSize, margin) = (15,10,20,25)
    return (rows, cols, cellSize, margin)
def appStarted(app):
    (rows, cols, cellSize, margin)=gameDimensions()
    app.fullRows = 0
    app.isGameOver = False
    app.timerDelay = 300 #500ms
    app.rows = rows
    app.cols = cols 
    app.cellSize = cellSize
    app.margin = margin
    app.emptyColor = 'blue'
    app.board = []
    for i in range(app.rows):
        app.board.append([])
        for j in range(app.cols):
            #j = app.emptyColor
            #app.board[i].insert(app.emptyColor,0)
            app.board[i].append(app.emptyColor)
    app.iPiece = [
        [  True,  True,  True,  True ]
    ]
    app.jPiece = [
        [  True, False, False ],
        [  True,  True,  True ]
    ]
    app.lPiece = [
        [ False, False,  True ],
        [  True,  True,  True ]
    ]
    app.oPiece = [
        [  True,  True ],
        [  True,  True ]
    ]
    app.sPiece = [
        [ False,  True,  True ],
        [  True,  True, False ]
    ]
    app.tPiece = [
        [ False,  True, False ],
        [  True,  True,  True ]
    ]
    app.zPiece = [
        [  True,  True, False ],
        [ False,  True,  True ]
    ]
    app.tetrisPieces = [ app.iPiece, app.jPiece, app.lPiece, app.oPiece, app.sPiece, app.tPiece, app.zPiece ]
    app.tetrisPieceColors = [ "red", "yellow", "magenta", "pink", "cyan", "green", "orange" ]
    newFallingPiece(app)
    score = 0
    #removeFullRows(app) #is this the right place?
    return
def newFallingPiece(app):
    randomIndex = random.randint(0, len(app.tetrisPieces) - 1)
    randomIndex2 = random.randint(0, len(app.tetrisPieceColors) - 1)
    app.fallingPiece = app.tetrisPieces[randomIndex]
    app.fallingPieceColor = app.tetrisPieceColors[randomIndex2]
    app.fallingPieceRow = 0
    array = []
    for i in range(len(app.fallingPiece)):
        for j in range(len(app.fallingPiece[i])):
            if i == 0 and app.fallingPiece[i][j] == True:
                array.append(app.fallingPiece[i][j])
            if i > 0 and app.fallingPiece[i][j] == True: 
                if app.fallingPiece[i-1][j] == False:
                    array.append(app.fallingPiece[i][j]) 
    app.numFallingPieceCols = len(array)
    app.fallingPieceCol = app.cols//2-app.numFallingPieceCols//2 
    return
def drawCell(app, canvas, row, col):
    return canvas.create_rectangle(app.margin+app.cellSize*col , app.margin+app.cellSize*row , app.cellSize*(col+1)+app.margin, app.cellSize*(row+1)+app.margin, fill = app.board[row][col], width = 3)
def drawCell2(app, canvas, row, col, color):
    return canvas.create_rectangle(app.margin+app.cellSize*(col+app.fallingPieceCol) , app.margin+app.cellSize*(row+app.fallingPieceRow) , app.cellSize*(col+1+app.fallingPieceCol)+app.margin, app.cellSize*(row+1+app.fallingPieceRow)+app.margin, fill = color, width = 3)
def drawBoard(app, canvas):
    for i in range(app.rows):
        for j in range(app.cols):
            drawCell(app, canvas, i, j)

def drawFallingPiece(app, canvas):
    for i in range(len(app.fallingPiece)): 
        for j in range(len(app.fallingPiece[i])): 
            if app.fallingPiece[i][j] == True:
                drawCell2(app,canvas, i , j, app.fallingPieceColor)
    return

def keyPressed(app, event):
    if event.key == "t":
        appStarted(app)
    if app.isGameOver != True:
        if event.key == "f":
            newFallingPiece(app)
        if event.key == "a":
            moveFallingPiece(app, 0, -1)
        if event.key == "d":
            moveFallingPiece(app, 0, 1)
        if event.key == "w":
            moveFallingPiece(app, -1, 0)
        if event.key == "s":
            moveFallingPiece(app, 1, 0)
        if event.key == "q":
            hardDrop(app)
            #moveFallingPiece(app, hardDrop(app), 0) #wrong change 10 to be the spaces between where the block currently is (app.fallingPieceRow?? and the deepest blue tile?)
        if event.key == "r":
            rotateFallingPiece(app)

def hardDrop(app):
    counter = 0
    while moveFallingPiece(app, 1, 0) == True:
        counter +=1
    #for drow in range(app.rows):
        #if moveFallingPiece(app, drow, 0) == True:
            #counter +=1
    moveFallingPiece(app, counter, 0)
    return

def moveFallingPiece(app, drow, dcol):
    app.fallingPieceCol += dcol
    app.fallingPieceRow += drow
    if fallingPieceIsLegal(app) == False:
        app.fallingPieceCol += -dcol
        app.fallingPieceRow += -drow
        return False
    else: 
        return True
        
def fallingPieceIsLegal(app):
    array1 = []
    count = 0
    for i in range(len(app.fallingPiece)):
        for j in range(len(app.fallingPiece[i])):
            if app.fallingPiece[i][j] == True: 
                count +=1
                if 0 <= i+app.fallingPieceRow < app.rows and 0 <= j+app.fallingPieceCol < app.cols:
                    if app.board[i+app.fallingPieceRow][j+app.fallingPieceCol] == app.emptyColor: 
                        array1.append("True")
                    else: 
                        return False
    if array1 == ["True"] * count:
        return True
    else: 
        return False

def rotateFallingPiece(app):
    oldpiece = copy.deepcopy(app.fallingPiece)
    oldRow = app.fallingPieceRow 
    oldNumRows = len(app.fallingPiece)
    newNumRows = len(app.fallingPiece[0])
    oldCol = app.fallingPieceCol
    oldNumCols = len(app.fallingPiece[0])
    newNumCols = len(app.fallingPiece)
    oldrows = len(app.fallingPiece)
    oldcols = len(app.fallingPiece[0])
    array2 = []
    newRow = oldRow + oldNumRows//2 - newNumRows//2
    newCol = oldCol + oldNumCols//2 - newNumCols//2
    for i in range(oldcols): 
        array2.append([])
    for k in range(oldrows):
        for l in range(oldcols):
            array2[(oldcols-1)-l].insert(k, app.fallingPiece[k][l]) 
    app.fallingPiece = array2
    app.fallingPieceRow = newRow
    app.fallingPieceCol = newCol
    if fallingPieceIsLegal(app) == False:
        app.fallingPiece = oldpiece
        app.fallingPieceRow = oldRow
        app.fallingPieceCol = oldCol
    return

def placeFallingPiece(app):
    for i in range(len(app.fallingPiece)): 
        for j in range(len(app.fallingPiece[i])): 
            if app.fallingPiece[i][j] == True: 
                app.board[app.fallingPieceRow+i][app.fallingPieceCol+j] = app.fallingPieceColor 
    return 

def removeFullRows(app):
    for i in range(app.rows):
        colorcounter = 0
        for j in range(app.cols):
            if app.board[i][j] != app.emptyColor:
                colorcounter += 1 
            if colorcounter == app.cols:
                app.board.pop(i)
                app.board.insert(0, [app.emptyColor]*len(app.board))
                app.fullRows += 1
    return

def drawScore(app,canvas):
    score = app.fullRows ** 2
    canvas.create_text(app.width/2, app.margin/2, text = f'Score: {score}', font = "Arial 13 bold")

def redrawAll(app, canvas):
    canvas.create_rectangle(0,0,app.width, app.height, fill = 'orange')
    drawBoard(app,canvas)
    drawFallingPiece(app, canvas)
    drawScore(app,canvas)
    if app.isGameOver == True:
        canvas.create_rectangle(0,0,app.width, app.height, fill = 'orange')
        canvas.create_text(app.width/2, app.height/2, text = "Game Over", font = "Arial 26 bold")
        canvas.create_text(app.width/2, app.height/2+app.margin, text = "Press T to Restart", font = "Arial 13 bold")

def playTetris():
    (rows, cols, cellSize, margin) = gameDimensions()
    runApp(width= cols*cellSize + margin*2, height = rows*cellSize+margin*2)
    return
#################################################
# main
#################################################

def main():
    #cs112_m20_unit8_linter.lint()
    playTetris()

if __name__ == '__main__':
    main()

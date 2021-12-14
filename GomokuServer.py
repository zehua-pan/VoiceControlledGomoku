"""
ECE 5725 Fall 2021
Final Project

VoiceControlledGomoku
Zehua Pan(zp74) and Yuhao Lu(yl3539)

"""

"""
This class is the "backend" of Gomoku. It is used to store 
the data of the game and recognize the game result every time 
players make a move.
"""
class GomokuServer:
    # each tuple record (dx, dy), which is 
    dirs = (
        ((-1, 0), (1, 0)),  # horizontal line, left and right direction 
        ((0, -1), (0, 1)),  # vertical line, up and down direction
        ((-1, -1), (1, 1)), # anti-diagonal line
        ((-1, 1), (1, -1))  # diagonal line
    )

    def __init__(self, rows=15, cols=15, nToWin=5, players="wb", blank="."):
        self.rows       = rows 
        self.cols       = cols 
        self.moveTimes  = 0
        self.lastMove   = None
        self.nToWin     = nToWin
        # define two 2D boards for two players
        self.boards     = [[[0] * cols for _ in range(rows)] for i in range(2)]
        self.players    = players
        self.blank      = '.'

    def lastPlayer(self):
        return self.players[(self.moveTimes-1)&1]

    def getNumOfSamePieces(self, dx, dy):
        # use self.moveTimes - 1, because we define moveTimes from 0
        # when player 0 play, the next player is 1, we judge result from 
        # the action of player 0, in this case, we should use the board 
        # of player 0, 
        lastBoard = self.boards[(self.moveTimes-1)&1]
        y, x = self.lastMove
        number = 0

        # if last_board[y][x] == 1, the correspond spot has a piece
        while self.inBounds(y, x) and lastBoard[y][x]:
            number += 1
            y += dy
            x += dx
        return number

    def gameOver(self):
        return self.moveTimes >= self.nToWin * 2 - 1 and any(
            (self.getNumOfSamePieces(*half1) + 
             self.getNumOfSamePieces(*half2) - 1 >= self.nToWin)
            for half1, half2 in self.dirs
        )

    def isDraw(self):
        return self.moveTimes >= self.rows * self.cols and not self.gameOver()

    def inBounds(self, row, col):
        return row >= 0 and row < self.rows and col >= 0 and col < self.cols
        
    def isEmpty(self, row, col):
        return not any(board[row][col] for board in self.boards)

    def move(self, row, col):
        if self.inBounds(row, col) and self.isEmpty(row, col):
            self.boards[self.moveTimes&1][row][col] = 1
            self.moveTimes += 1
            self.lastMove = row, col
            return True
        return False

    #  def charForCell(self, row, col):
    #      for i, char in enumerate(self.players):
    #          if self.boards[i][row][col]:
    #              return char
    #      return self.blank
    #
    #  def toGrid(self):
    #      return [
    #          [self.charForCell(row, col) for col in range(self.cols)]
    #          for row in range(self.rows)
    #      ]
    #
    #  # print game board
    #  def __repr__(self):
    #      boardGrid = self.toGrid()
    #      return "\n".join([" ".join(lineChars) for lineChars in boardGrid])
    #

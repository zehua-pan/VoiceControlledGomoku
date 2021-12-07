from itertools import chain
import pygame
from GomokuServer import GomokuServer
from InputHandler import InputHandler
import globalParamters as gp
import os

# piTFT env
os.putenv('SDL_VIDEORIVER', 'fbcon')
os.putenv('SDL_FBDEV', '/dev/fb1')

class Colors:
    BLACK = 0, 0, 0
    WHITE = 255, 255, 255
    BROWN = 205, 128, 0
    RED   = 100, 255, 100

class Gomoku:
    def __init__(
        self,
        unit=60,
        rows=15,
        cols=15,
        nToWin=5,
        pieceSize=40,
        onTFT=False
    ):
        self.ratio = 1
        self.unit = unit
        # piTFT screen size
        self.screenWidth = 320
        self.screenHeight = 240
        # convert unit to fit piTFT
        if(onTFT): convertDisplayScale(onTFT)
        
        # parameters for Gomoku GUI
        self.fontSize = self.ratio*20
        self.halfUnit = self.unit // 2
        self.rows = rows
        self.cols = cols
        self.nToWin = nToWin
        self.width = cols * self.unit
        self.borderWidth = self.width+20
        self.height = rows * self.unit
        self.borderHeight = self.height+40
        self.pieceSize = 15*self.ratio
        self.lineWidth = 2*self.ratio
        self.gameMsg = 'Please play the game use your voice'
        # pygame data members
        pygame.init()
        pygame.display.set_caption("Gomoku")
        self.font = pygame.font.SysFont('arial', self.fontSize)
        self.screen = pygame.display.set_mode((self.borderWidth,self.borderHeight))
        self.screen.fill(Colors.WHITE)
        # variable members
        self.gomokuServer = GomokuServer(rows=rows, cols=cols, nToWin=nToWin)
        self.inputHandler = InputHandler(rows, cols)
        # FSM, state : idle, running, again, exit
        self.state = "idle"
        
    def convertDisplayScale(self,onTFT):
        if(onTFT):
            curUnit = min((self.screenWidth-20)//self.cols, (self.screenHeight-40)//self.rows)
            self.ratio = curUnit//self.unit 
            self.unit = curUnit


    def drawLineNumbers(self):
        #draw rows
        for i in range(self.rows):
            text_surface = self.font.render(str(i), True, Colors.WHITE)
            rect = text_surface.get_rect(center=(i*self.unit+self.halfUnit,self.height-5))
            self.screen.blit(text_surface,rect)
        #draw cols
        for j in range(self.cols):
            text_surface = self.font.render(str(j), True, Colors.WHITE)
            rect = text_surface.get_rect(center=(self.width-5,j*self.unit+self.halfUnit))
            self.screen.blit(text_surface,rect)

    def hintMsg(self,msg="none"):
        text_surface = self.font.render(msg, True, Colors.RED)
        rect = text_surface.get_rect(center=(self.width//2,self.height+20))
        pygame.draw.rect(self.screen, Colors.BROWN, pygame.Rect(0,self.height+5,self.width,self.height))
        self.screen.blit(text_surface,rect)

    def drawRowLines(self):
        for y in range(self.halfUnit, self.height, self.unit):
            yield (self.halfUnit, y), (self.width - self.halfUnit, y)

    def drawColLines(self):
        for x in range(self.halfUnit, self.width, self.unit):
            yield (x, self.halfUnit), (x, self.height - self.halfUnit)

    def drawLines(self):
        allLines = chain(self.drawRowLines(), self.drawColLines())
        for start, end in allLines:
            pygame.draw.line(self.screen, Colors.BLACK, start, end, self.lineWidth)

    def drawBackground(self):
        rect = pygame.Rect(0, 0, self.borderWidth, self.borderHeight)
        pygame.draw.rect(self.screen, Colors.BROWN, rect)

    def drawBoard(self):
        self.drawBackground()
        self.drawLines()
        self.drawLineNumbers()
        self.hintMsg(self.gameMsg)

    def drawPiece(self, row, col):
        pieceX = col * self.unit + self.halfUnit
        pieceY = row * self.unit + self.halfUnit
        if self.gomokuServer.lastPlayer() == 'w':
            color = Colors.WHITE
        else:
            color = Colors.BLACK
        pygame.draw.circle(self.screen, color, (pieceX, pieceY), self.pieceSize)
        
    def sendLEDColors(self):
        FIFO_PATH = gp.FIFO_LED
        # if lastPlayer is white, current player should be black, vice versa
        userColor = "Black" if self.gomokuServer.lastPlayer() == 'w' else "White"
        os.system(f'echo "{userColor}" > {FIFO_PATH}')

    def showOutcome(self):
        print("show outcome of this game")
        playerNames = {"w":"White", "b":"Black"}
        player      = playerNames[self.gomokuServer.lastPlayer()]
        text = "draw!" if self.gomokuServer.isDraw() else f"{player} wins!"
        fontSize = self.width // 10
        font = pygame.font.Font(None, fontSize)
        text_surface = font.render(text, True, Colors.WHITE, Colors.BLACK)
        textX = self.width // 2 - text_surface.get_width() // 2
        textY = self.height // 2 - text_surface.get_height() // 2
        self.screen.blit(text_surface, (textX, textY))

    def waitAfterFinish(self):
        """
        For this function, we only need to listen the again command or exit command
        """
        print("current game finish, wait for next command")
        while True:
            isCMD_Valid, userRow, userCol, newMsg = self.inputHandler.getCommand()
            if self.handleSpecialCMD(newMsg) == "again": return
            self.sendLEDColors()
        
    def makeMove(self, row, col):
        if self.gomokuServer.move(row, col):
            self.drawPiece(row, col)

    def handleSpecialCMD(self, command):
        if(command == 'exit'): 
            pygame.quit()
            exit(1)
        elif(command == 'again'):
            self.state = "again"
        return self.state

    def play(self):
        self.state = "running"
        # set framerate
        pygame.time.Clock().tick(10)
        # initialize GUI
        self.drawBoard()
        pygame.display.flip()
        # set LED
        self.sendLEDColors()
        newMsg = ''

        # FSM, recieve->handle->send feedback->receive...
        while not self.gomokuServer.gameOver() and not self.gomokuServer.isDraw():
            # capture speech events, this part can be extracted as/in a class
            isCMD_Valid, userRow, userCol, newMsg = self.inputHandler.getCommand()
            # handle events
            if self.handleSpecialCMD(newMsg) == "again": return
            if(isCMD_Valid):
                self.makeMove(userRow, userCol)
            self.hintMsg(newMsg.capitalize())
            pygame.display.flip()
            # send feedback to speechrecogition
            self.sendLEDColors()
            
        self.showOutcome()
        pygame.display.flip()
        self.waitAfterFinish()

if __name__ == "__main__":
    while True:
        game = Gomoku(rows=10, cols=10, nToWin=2)
        game.play()





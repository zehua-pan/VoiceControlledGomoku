from itertools import chain
import pygame
from GomokuServer import GomokuServer

class Colors:
    BLACK = 0, 0, 0
    WHITE = 255, 255, 255
    BROWN = 205, 128, 0

class Gomoku:
    def __init__(
        self,
        unit=60,
        rows=15,
        cols=15,
        nToWin=5,
        pieceSize=40
    ):
        
        self.unit = unit
        self.fontSize = 20
        self.halfUnit = unit // 2
        self.rows = rows
        self.cols = cols
        self.nToWin = nToWin
        self.width = cols * unit
        self.borderWidth = self.width+20
        self.height = rows * unit
        self.borderHeight = self.height+40
        self.pieceSize = 15
        pygame.init()
        pygame.display.set_caption("Gomoku")
        self.screen = pygame.display.set_mode((self.borderWidth, self.borderHeight))
        self.font = pygame.font.SysFont('arial', self.fontSize)
        self.screen.fill(Colors.WHITE)
        self.gomokuServer = GomokuServer(rows=rows, cols=cols, nToWin=nToWin)

    def drawLabels(self):
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

    def hintMsg(self,msg):
            text_surface = self.font.render(msg, True, Colors.WHITE)
            rect = text_surface.get_rect(center=(self.width//2,self.height+20))
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
            pygame.draw.line(self.screen, Colors.BLACK, start, end, width=2)

    def drawBackground(self):
        rect = pygame.Rect(0, 0, self.borderWidth, self.borderHeight)
        pygame.draw.rect(self.screen, Colors.BROWN, rect)

    def drawBoard(self):
        self.drawBackground()
        self.drawLines()
        self.drawLabels()

    def drawPiece(self, row, col):
        pieceX = col * self.unit + self.halfUnit
        pieceY = row * self.unit + self.halfUnit
        if self.gomokuServer.lastPlayer() == 'w':
            color = Colors.WHITE
        else:
            color = Colors.BLACK
        pygame.draw.circle(self.screen, color, (pieceX, pieceY), self.pieceSize)

    def showOutcome(self):
        playerNames = {"w":"White", "b":"Black"}
        player      = playerNames[self.gomokuServer.lastPlayer()]
        text = "draw!" if self.gomokuServer.isDraw() else f"{player} wins!"
        fontSize = self.width // 10
        font = pygame.font.Font(None, fontSize)
        text_surface = font.render(text, True, Colors.WHITE, Colors.BLACK)
        textX = self.width // 2 - text_surface.get_width() // 2
        textY = self.height // 2 - text_surface.get_height() // 2
        self.screen.blit(text_surface, (textX, textY))

    def exitOnClick(self):
        while True:
            for event in pygame.event.get():
                if (event.type == pygame.QUIT or 
                        event.type == pygame.MOUSEBUTTONDOWN):
                    pygame.quit()
                    return

    def makeMove(self, x, y):
        row = y // self.unit
        col = x // self.unit
        if self.gomokuServer.move(row, col):
            self.drawPiece(row, col)
        
    def play(self):
        # set framerate
        pygame.time.Clock().tick(10)
        self.drawBoard()
        pygame.display.flip()

        while not self.gomokuServer.gameOver() and not self.gomokuServer.isDraw():
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.makeMove(*event.pos)
                    pygame.display.flip()
            self.hintMsg('lol')
        self.showOutcome()
        pygame.display.flip()
        self.exitOnClick()

if __name__ == "__main__":
    game = Gomoku(rows=10, cols=10, nToWin=5)
    game.play()





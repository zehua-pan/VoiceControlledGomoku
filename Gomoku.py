import itertools
import pygame

from gomoku_position import GomokuPosition

class Colors:
    BLACK = 0, 0, 0
    WHITE = 255, 255, 255
    BROWN = 205, 128, 0


class Gomoku:
    def __init__(
        self,
        size=60,
        piece_size=20,
        rows=15,
        cols=15,
        n_to_win=5,
        caption="Gomoku"
    ):
        self.rows = rows
        self.cols = cols
        self.w = rows * size
        self.h = cols * size
        self.size = size
        self.piece_size = piece_size
        self.half_size = size // 2
        pygame.init()
        pygame.display.set_caption(caption)
        self.screen = pygame.display.set_mode((self.w, self.h))
        self.screen.fill(Colors.WHITE)
        self.player_colors = {"w": Colors.WHITE, "b": Colors.BLACK}
        self.player_names = {"w": "White", "b": "Black"}
        self.board = GomokuPosition(rows, cols, n_to_win)

    def row_lines(self):
        half = self.half_size

        for y in range(half, self.h - half + self.size, self.size):
            yield (half, y), (self.w - half, y)

    def col_lines(self):
        half = self.half_size

        for x in range(half, self.w - half + self.size, self.size):
            yield (x, half), (x, self.h - half)
        
    def draw_background(self):
        rect = pygame.Rect(0, 0, self.w, self.h)
        pygame.draw.rect(self.screen, Colors.BROWN, rect)

    def draw_lines(self):
        lines = itertools.chain(self.col_lines(), self.row_lines())

        for start, end in lines:
            pygame.draw.line(
                self.screen, 
                Colors.BLACK, 
                start, 
                end, 
                width=2
            )

    def draw_board(self):
        self.draw_background()
        self.draw_lines()
        
    def draw_piece(self, row, col):
        player = self.board.last_player()
        circle_pos = (
           col * self.size + self.half_size, 
           row * self.size + self.half_size,
        )
        pygame.draw.circle(
           self.screen, 
           self.player_colors[player], 
           circle_pos, 
           self.piece_size
        )

    def show_outcome(self):
        player = self.player_names[self.board.last_player()]
        msg = "draw!" if self.board.is_draw() else f"{player} wins!"
        font_size = self.w // 10
        font = pygame.font.Font("freesansbold.ttf", font_size)
        label = font.render(msg, True, Colors.WHITE, Colors.BLACK)
        x = self.w // 2 - label.get_width() // 2
        y = self.h // 2 - label.get_height() // 2
        self.screen.blit(label, (x, y))

    def exit_on_click(self):
        while True:
            for event in pygame.event.get():
                if (event.type == pygame.QUIT or 
                        event.type == pygame.MOUSEBUTTONDOWN):
                    pygame.quit()
                    return

    def make_move(self, x, y):
        col = x // self.size
        row = y // self.size
        
        if self.board.move(row, col):
            self.draw_piece(row, col)
        
    def play(self):
        pygame.time.Clock().tick(10)
        self.draw_board()
        pygame.display.update()

        while not self.board.just_won() and not self.board.is_draw():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.make_move(*event.pos)
                    pygame.display.update()
        
        self.show_outcome()
        pygame.display.update()
        self.exit_on_click()

if __name__ == "__main__":
    game = Gomoku(rows=10, cols=10, n_to_win=5)
    game.play()

class GomokuPosition:
    dirs = (
        ((0, -1), (0, 1)), 
        ((1, 0), (-1, 0)),
        ((1, 1), (-1, -1)),
        ((1, -1), (-1, 1)),
    )

    def __init__(self, rows, cols, n_to_win, players="wb", blank="."):
        self.ply = 0
        self.rows = rows
        self.cols = cols
        self.last_move = None
        self.n_to_win = n_to_win
        self.boards = [[[0] * cols for _ in range(rows)] for i in range(2)]
        self.players = players
        self.blank = blank

    def board(self, row=None, col=None):
        if row is None and col is None:
            return self.boards[self.ply&1]
        elif col is None:
            return self.boards[self.ply&1][row]

        return self.boards[self.ply&1][row][col]

    def move(self, row, col):
        if self.in_bounds(row, col) and self.is_empty(row, col):
            self.board(row)[col] = 1
            self.ply += 1
            self.last_move = row, col
            return True

        return False

    def is_empty(self, row, col):
        return not any(board[row][col] for board in self.boards)

    def in_bounds(self, y, x):
        return y >= 0 and y < self.rows and x >= 0 and x < self.cols

    def count_from_last_move(self, dy, dx):
        if not self.last_move:
            return 0

        last_board = self.boards[(self.ply-1)&1]
        y, x = self.last_move
        run = 0

        while self.in_bounds(y, x) and last_board[y][x]:
            run += 1
            x += dx
            y += dy
        
        return run

    def just_won(self):
        return self.ply >= self.n_to_win * 2 - 1 and any(
            (self.count_from_last_move(*x) + 
             self.count_from_last_move(*y) - 1 >= self.n_to_win)
            for x, y in self.dirs
        )
        
    def is_draw(self):
        return self.ply >= self.rows * self.cols and not self.just_won()

    def last_player(self):
        if self.ply < 1:
            raise IndexError("no moves have been made")

        return self.players[(self.ply-1)&1]

    def char_for_cell(self, row, col):
        for i, char in enumerate(self.players):
            if self.boards[i][row][col]:
                return char
        
        return self.blank

    def to_grid(self):
        return [
            [self.char_for_cell(row, col) for col in range(self.cols)]
            for row in range(self.rows)
        ]

    def __repr__(self):
        return "\n".join([" ".join(row) for row in self.to_grid()])


if __name__ == "__main__":
    pos = GomokuPosition(rows=4, cols=4, n_to_win=3)

    while not pos.just_won() and not pos.is_draw():
        print(pos, "\n")

        try:
            if not pos.move(*map(int, input("[row col] :: ").split())):
                print("try again")
        except (ValueError, IndexError):
            print("try again")

    print(pos, "\n")
        
    if pos.just_won():
        print(pos.last_player(), "won")
    else:
        print("draw")

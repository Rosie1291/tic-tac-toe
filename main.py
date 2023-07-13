import pygame as pg
import sys
from random import randint

# global constants
WIN_SIZE = 900  # set window's size
CELL_SIZE = WIN_SIZE // 9  # set cell's size
INF = float('inf')  # start with empty cells
vec2 = pg.math.Vector2
CELL_CENTER = vec2(CELL_SIZE / 2)


# TicTacToe game class
class TicTacToe:
    def __init__(self, game):
        self.game = game
        # scale the images
        self.board_image = self.get_scaled_image(path='resources/board.png', res=[WIN_SIZE] * 2)
        self.O_image = self.get_scaled_image(path='resources/o.png', res=[CELL_SIZE] * 2)
        self.X_image = self.get_scaled_image(path='resources/x.png', res=[CELL_SIZE] * 2)

        # initialize game variables
        self.game_array = [[INF for _ in range(9)] for _ in range(9)]  # start with empty 9x9 grid
        self.player = randint(0, 1)  # randomly assign the first player
        self.winner = None
        self.game_steps = 0
        self.font = pg.font.SysFont('Arial', CELL_SIZE // 4, True)

    def check_winner(self):
        # check if there's a winner
        for player in [0, 1]:
            for i in range(9):
                for j in range(6):
                    # check horizontal and vertical lines
                    if all(self.game_array[i][j + k] == player for k in range(4)):
                        self.winner = 'OX'[player]
                        self.winning_cells = sorted([(i, j + k) for k in range(4)])
                        return
                    if all(self.game_array[j + k][i] == player for k in range(4)):
                        self.winner = 'OX'[player]
                        self.winning_cells = sorted([(j + k, i) for k in range(4)])
                        return
            for i in range(6):
                for j in range(6):
                    # check diagonals
                    if all(self.game_array[i + k][j + k] == player for k in range(4)):
                        self.winner = 'OX'[player]
                        self.winning_cells = sorted([(i + k, j + k) for k in range(4)])
                        return
                    if all(self.game_array[i + 3 - k][j + k] == player for k in range(4)):
                        self.winner = 'OX'[player]
                        self.winning_cells = sorted([(i + 3 - k, j + k) for k in range(4)], reverse=True)
                        return

    def run_game_process(self):
        # handle mouse input for placing a marker
        current_cell = vec2(pg.mouse.get_pos()) // CELL_SIZE
        col, row = map(int, current_cell)
        left_click = pg.mouse.get_pressed()[0]

        if left_click and self.game_array[row][col] == INF and not self.winner:
            self.game_array[row][col] = self.player
            self.player = not self.player
            self.game_steps += 1
            self.check_winner()

    def draw_objects(self):
        # draw the game state on screen
        for y, row in enumerate(self.game_array):
            for x, obj in enumerate(row):
                if obj != INF:
                    self.game.screen.blit(self.X_image if obj else self.O_image, vec2(x, y) * CELL_SIZE)

    def draw_winner(self):
        # display winner on screen
        if self.winner:
            label = self.font.render(f'Player "{self.winner}" wins!', True, 'red', 'white')
            self.game.screen.blit(label, (WIN_SIZE // 2 - label.get_width() // 2, WIN_SIZE // 8))

    def draw_winning_line(self):
        if self.winner:
            # reverse coordinates to match Pygame's coordinate system
            start = vec2(self.winning_cells[0][::-1]) * CELL_SIZE + vec2(CELL_SIZE / 2)
            end = vec2(self.winning_cells[-1][::-1]) * CELL_SIZE + vec2(CELL_SIZE / 2)
            pg.draw.line(self.game.screen, (255, 0, 0), start, end, 10)

    def draw(self):
        self.game.screen.blit(self.board_image, (0, 0))  # draw board
        self.draw_objects()  # draw Xs and Os
        self.draw_winning_line()  # draw the winning sequence
        self.draw_winner()  # display result

    @staticmethod
    def get_scaled_image(path, res):
        img = pg.image.load(path)
        return pg.transform.scale(img, res)

    def print_caption(self):
        # display which player's turn in the window caption
        pg.display.set_caption(f'Player "{"OX"[self.player]}" turn!')
        if self.winner:
            pg.display.set_caption(f'Player "{self.winner}" wins! Press Space to Restart')
        # if all cells filled without winner, it's a draw
        elif self.game_steps == 81:
            pg.display.set_caption(f'Draw! Press Space to Restart')

    def run(self):
        self.print_caption() # show current status in window caption
        self.draw()
        self.run_game_process()


class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode([WIN_SIZE] * 2)
        self.clock = pg.time.Clock() # clock to control frame rate
        self.tic_tac_toe = TicTacToe(self) # create a tictactoe game

    def new_game(self):
        self.tic_tac_toe = TicTacToe(self)

    def check_events(self):
        for event in pg.event.get():
            # exit if game is quit
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            # start new game if spacebar is pressed
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.new_game()

    def run(self):
        #  game loop
        while True:
            self.tic_tac_toe.run()
            self.check_events()
            pg.display.update()
            self.clock.tick(60)


if __name__ == '__main__':
    # create a new game instance and run the game
    game = Game()
    game.run()

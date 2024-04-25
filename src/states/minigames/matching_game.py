import random

import pygame as pg

from src.constants import *
from src.states.minigames.minigame import Minigame

white = (255, 255, 255)
black = (0, 0, 0)
gray = (128, 128, 128)
green = (0, 255, 0)
blue = (0, 0, 255)


class Matching(Minigame):
    """A minigame where you must match """

    def __init__(self):
        instructions = "The goal of this minigame is to select the boxes with matching numbers. You must get 5 matches within 25 turns"
        super().__init__(instructions)

        # self.timer = pg.time.Clock()
        self.screen = pg.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
        self.title_font = pg.font.Font('freesansbold.ttf', 56)
        self.small_font = pg.font.Font('freesansbold.ttf', 26)
        self.rows = 4
        self.cols = 6
        self.correct = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0]]
        self.new_board = True
        self.options_list = []
        self.spaces = []
        self.used = []
        self.first_guess = False
        self.second_guess = False
        self.first_guess_num = 0
        self.second_guess_num = 0
        self.board = []
        self.score = 0
        self.matches = 0
        self.win_text = ""

    def handle_events(self, events):
        super().handle_events(events)  # To enable pause menu access

        if self.new_board:
            self.generate_board()
            self.new_board = False

        if self.first_guess and self.second_guess:
            self.check_guesses(self.first_guess_num, self.second_guess_num)
            pg.time.delay(700)
            self.first_guess = False
            self.second_guess = False

        for event in events:
            if event.type == pg.MOUSEBUTTONDOWN:
                for i in range(len(self.board)):
                    button = self.board[i]
                    if button.collidepoint(event.pos) and not self.first_guess:
                        self.first_guess = True
                        self.first_guess_num = i
                    if button.collidepoint(
                            event.pos) and not self.second_guess and self.first_guess and i != self.first_guess_num:
                        self.second_guess = True
                        self.second_guess_num = i
            if self.matches == 5:  # Value of required matches to win, currently set to the entire board
                self.won = True
                self.win_text = f"You did it in {self.score} moves"
            elif self.score > 25:  # Value of number of attempts before losing
                self.won = False

    def update(self, events):
        super().update(events)

    def generate_board(self):
        """Randomly generates the board."""

        for item in range(self.rows * self.cols // 2):
            self.options_list.append(item)

        for item in range(self.rows * self.cols):
            piece = self.options_list[random.randint(0, len(self.options_list) - 1)]
            self.spaces.append(piece)
            if piece in self.used:
                self.used.remove(piece)
                self.options_list.remove(piece)
            else:
                self.used.append(piece)

    def check_guesses(self, first, second):
        """
        Adds to the score if the user picked the same number in both of
        their guesses.

        Args:
            first (int): The first guess the user picked.
            second (int): The second guess the user picked.
        """

        if self.spaces[first] == self.spaces[second]:
            col1 = first // self.rows
            col2 = second // self.rows
            row1 = first - (first // self.rows * self.rows)
            row2 = second - (second // self.rows * self.rows)
            if self.correct[row1][col1] == 0 and self.correct[row2][col2] == 0:
                self.correct[row1][col1] = 1
                self.correct[row2][col2] = 1
                self.score += 1
                self.matches += 1

        else:
            self.score += 1

    def draw(self):
        super().draw()  # Draw minigame background
        self.draw_backgrounds()
        self.board = self.draw_board()

        if self.first_guess:
            piece_text = self.small_font.render(f'{self.spaces[self.first_guess_num]}', True, blue)
            location = (self.first_guess_num // self.rows * 100 + 110,
                        (self.first_guess_num - (self.first_guess_num // self.rows * self.rows)) * 90 + 165)
            self.screen.blit(piece_text, (location))

        if self.second_guess:
            piece_text = self.small_font.render(f'{self.spaces[self.second_guess_num]}', True, blue)
            location = (self.second_guess_num // self.rows * 100 + 110,
                        (self.second_guess_num - (self.second_guess_num // self.rows * self.rows)) * 90 + 165)
            self.screen.blit(piece_text, (location))

    def draw_backgrounds(self):
        """Draws the minigame background and text."""

        top_menu = pg.draw.rect(self.screen, black, [0, 0, SCREEN_WIDTH, 100])
        title_text = self.title_font.render('The matching game!', True, white)
        self.screen.blit(title_text, (80, 20))
        board_space = pg.draw.rect(self.screen, gray, [0, 100, SCREEN_WIDTH, SCREEN_HEIGHT - 200], 0)
        bottom_menu = pg.draw.rect(self.screen, black, [0, SCREEN_HEIGHT - 100, SCREEN_WIDTH, 100], 0)
        score_text = self.small_font.render(f'Current Turns: {self.score}', True, white)
        self.screen.blit(score_text, (550, 520))

    def draw_board(self):
        """Draws the board onto the screen.

        Returns:
            list[pygame.Rect]: List of `Rect` objects for each piece on the 
                board.
        """
        board_list = []
        for i in range(self.cols):
            for j in range(self.rows):
                index = i * self.rows + j
                if index < len(self.spaces):
                    piece = pg.draw.rect(self.screen, white, [i * 100 + 100, j * 90 + 152, 50, 50], 0, 4)
                    board_list.append(piece)
                    # piece_text = self.small_font.render(f'{self.spaces[index]}', True, gray)
                    # self.screen.blit(piece_text, (i * 100 + 106, j * 90 + 140))

        for i in range(self.rows):
            for j in range(self.cols):
                if self.correct[i][j] == 1:
                    piece = pg.draw.rect(self.screen, green, [j * 100 + 98, i * 90 + 150, 54, 54], 3, 4)
                    piece_text = self.small_font.render(f'{self.spaces[j * self.rows + i]}', True, black)
                    self.screen.blit(piece_text, (j * 100 + 110, i * 90 + 165))

        return board_list

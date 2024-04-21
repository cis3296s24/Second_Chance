import pygame as pg
import os
import random

from src.states.minigames.minigame import Minigame

from pygame.locals import *


class Calculate(Minigame):
    """A minigame to test your memory."""

    def __init__(self):
        instructions = (
            "The goal for this miniGame is to calculate the correct answer."
        )

        img = "calculate.png"

        super().__init__(
            instructions,
            img=os.path.join("minigames", img)
        )

        # Minigame specific attributes
        self.generated_string = ""
        self.input_string = ""
        self.input_rect = pg.Rect(300, 282, 200, 36)  # Adjusted position to center vertically
        self.input_active = False
        self.font = pg.font.SysFont(None, 36)
        self.generated_text_surf = None
        self.display_time = 10
        self.display_timer = 0  
        self.is_string_currently_displayed = False
        self.was_string_displayed_yet = False
        self.clock = pg.time.Clock()
        self.firstNum = 0
        self.secondNum = 0
        self.sign = ''
            
    def handle_events(self, events):
        super().handle_events(events) # To enable pause menu access
        for event in events:
            if event.type == pg.KEYDOWN and self.input_active:
                if event.key == pg.K_RETURN:
                    self.check_win_condition()
                elif event.key == pg.K_BACKSPACE:
                    self.input_string = self.input_string[:-1]
                else:
                    self.input_string += event.unicode

    def update(self, events):
        super().update(events)
        if not self.was_string_displayed_yet:
            self.generated_string = self.generate_random_question()
            self.generated_text_surf = self.font.render(self.generated_string, True, (255, 255, 255))
            self.was_string_displayed_yet = True
            self.is_string_currently_displayed = True
            self.display_timer = self.display_time * 1000  # Convert seconds to milliseconds
            self.input_active = True

    def draw(self):
        super().draw() # Draw minigame background
        
        if self.generated_text_surf:
            self.screen.blit(self.generated_text_surf, ((self.screen.get_width() - self.generated_text_surf.get_width()) / 2 + 30, 200))

            pg.draw.rect(self.screen, (255, 255, 255), self.input_rect, 2)
            input_text_surf = self.font.render(self.input_string, True, (255, 255, 255))
            self.screen.blit(input_text_surf, (self.input_rect.x + 5, self.input_rect.y + 5))

    def generate_random_question(self):
        # genrate the question
        self.firstNum = random.randint(1,20)
        self.secondNum = random.randint(1,20)
        self.sign = self.generate_sign()
        question = '{}{}{}='.format(self.firstNum,self.sign,self.secondNum)
        return question

    def generate_sign(self):
        # genrate different question type
        sign = random.randint(1,3)
        match(sign):
            case 1:
                return '+'
            case 2:
                return '-'
            case 3:
                return 'x'
            
            case default:
                return 'something went wrong'


    def check_win_condition(self):
        # check the player enter the correct answer
        if(self.sign == '+'):
            if (self.firstNum + self.secondNum == int(self.input_string)):
                self.won = True
                self.win_text = "\\o/"
            else:
                self.won = False
        if(self.sign == '-'):
            if (self.firstNum - self.secondNum == int(self.input_string)):
                self.won = True
                self.win_text = "\\o/"
            else:
                self.won = False
        if(self.sign == 'x'):
            if (self.firstNum * self.secondNum == int(self.input_string)):
                self.won = True
                self.win_text = "\\o/"
            else:
                self.won = False

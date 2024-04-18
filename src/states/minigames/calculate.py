import pygame as pg
import os
import random

from src.states.minigames.minigame import Minigame

from pygame.locals import *

class calculate(Minigame):
    """A minigame to test a basic calculation"""

    def __init__(self):
        instructions = (
            "The goal of this minigame is to calculate the currect answer."
            "Press number keys on your keyboard to enter your answer."
            )
        img = "calculate.jpg"
        super().__init__(
            instructions, 
            img = os.path.join("minigames",img)
        )

        #Minigame attritubes

        self.firstNum = 0
        self.secNum = 0
        self.answerType = 0
        self.questionTitle = ""
        self.userInput = ""
        self.display_Rect = pg.rect(200,200,200,200)
        self.enter_Rect = pg.rect(200,200,200,200)



        
    def handle_events(self, events):
        super().handle_events(events)
        for event in events:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    self.checkCorrect()
                elif event.type == pg.K_BACKSPACE:
                    self.userInput = self.userInput[:-1]
                else:
                    self.userInput += event.int
    def update(self, events):
        super().update(events)
        self.questionTitle = self.question()
        
    
    def draw(self):
        super().draw()

        self.screen.blit(self.questionTitle,((self.screen.get_width() - self.generated_text_surf.get_width()) / 2, 200))
        pg.draw.rect(self.screen, (255, 255, 255), self.enter_Rect, 2)
        enter_Rect_surf = self.font.render(self.enter_Rect, True, (255, 255, 255))
        self.screen.blit(enter_Rect_surf, (self.enter_Rect.x + 5, self.enter_Rect.y + 5))

            
    def question(self):
        questionType = random.randrange(3)
        first = random.randint(0,20)
        second = random.randint(0,20)
        self.firstNum = first
        self.secNum = second
        self.answerType = questionType
        match questionType:
            case 0:
                return f'{first} + {second} = '
            case 1:
                return f'{first} - {second} = '
            case 2:
                return f'{first} x {second} = '
            
    def checkCorrect(self, questionType):
        """Check if the user enter the correct answer. """
        if (questionType == 0):
            if int(self.userInput) == self.firstNum + self.secNum:
                self.won = True
            else:
                self.won = False
        elif(questionType == 1):
            if int(self.userInput) == self.firstNum - self.secNum:
                    self.won = True
            else:
                self.won = False
        elif(questionType == 2):
            if int(self.userInput) == self.firstNum * self.secNum:
                self.won = True
            else:
                self.won = False
        
            
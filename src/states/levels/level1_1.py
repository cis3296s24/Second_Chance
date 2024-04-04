import pygame as pg

from ..state import State
from src.entities.player import Player
from src.objects.platforms import Platform
import src.states.menu.menus as menus

class Level1_1(State):
    scroll = 0
    def __init__(self):
        super().__init__(None, 1)
        self.platforms = pg.sprite.Group()
        self.player = Player(100, 100, self.platforms, self.scroll)
        self.create_platforms()
    
    def handle_events(self, events):
        for event in events:
            if event.type != pg.KEYDOWN:
                return
            if event.key == pg.K_ESCAPE:
                self.manager.set_state(menus.StartMenu)
    
    def update(self, events):
        self.player.update()
    
    def draw(self):
        super().draw_bg()
        self.platforms.draw(self.screen)
        self.player.draw()
        
    def create_platforms(self):
        for i in range(1, 6):
            self.platforms.add(Platform(i * 100, i * 100))

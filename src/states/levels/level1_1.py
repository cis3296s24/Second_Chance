import pygame as pg
import time

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
        self.controls = pg.font.Font(None, 36).render(
            "Press 'Escape' to pause", True, "white")

        self.start_time = time.time()  #initialize starting time
    
    def handle_events(self, events):
        for event in events:
            if event.type != pg.KEYDOWN:
                return
            if event.key == pg.K_ESCAPE:
                self.manager.set_state(menus.PauseMenu, save_prev=True)
    
    def update(self, events):
        self.player.update()
        #calculate elapsed time
        self.elapsed_time = time.time() - self.start_time
    
    def draw(self):
        super().draw_bg()
        self.platforms.draw(self.screen)
        self.player.draw()
        self.draw_health_bar()
        self.screen.blit(self.controls, (20, 20))
        self.draw_timer()
        
    def create_platforms(self):
        for i in range(1, 6):
            self.platforms.add(Platform(i * 100, i * 100))

    def draw_timer(self):
        font = pg.font.Font(None, 36) 
        text_surface = font.render(f"Level 1 Time: {int(self.elapsed_time)}", True, (255, 255, 255))  
        text_rect = text_surface.get_rect(topright=(self.screen.get_width() - 10, 10))  #top right of screen
        self.screen.blit(text_surface, text_rect)  

    def draw_health_bar(self):
        # Calculate the width of the health bar based on current health
        health_bar_width = (self.player.health / self.player.max_health) * self.player.health_bar_length
        # Calculate the position of the health bar above the player
        health_bar_x = self.player.rect.x - (self.player.rect.width * (self.player.scale_factor - 1)) / 2
        health_bar_y = self.player.rect.y - 20  # Adjust this value to position the health bar properly
        # Draw the health bar
        pg.draw.rect(self.screen, (255, 0, 0), (health_bar_x, health_bar_y, self.player.health_bar_length, self.player.health_bar_height))
        pg.draw.rect(self.screen, self.player.health_bar_color, (health_bar_x, health_bar_y, health_bar_width, self.player.health_bar_height))


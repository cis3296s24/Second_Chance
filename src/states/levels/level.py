import pygame as pg
import time
import os

from ..state import State
from src.entities.player import Player
import src.states.menu.menus as menus
import src.entities.enemies.enemy as enemy

class Level(State):
    
    def __init__(self, level: int, music_file: str, imgArr=None):
        super().__init__()
        self.level = level
        self.scroll = 0
        self.init_sprites()
        self.init_attributes()
        self.init_background(imgArr)
        self.init_music(music_file)
        
    def handle_events(self, events):
        for event in events:
            if event.type != pg.KEYDOWN: # Ignore all inputs except key presses
                return
            if event.key == pg.K_ESCAPE: # Open pause menu
                self.manager.set_state(menus.PauseMenu, save_prev=True)
    
    def update(self, events):
        self.player.update()
        self.enemies.update(self.player)
        self.timer_update()
        self.health_update()
        
        # Check for collision between player's melee attacks and enemy
        collisions = pg.sprite.groupcollide(self.player.melee_attacks, self.enemies, False, False)  # Change False to True to remove the melee attack sprite upon collision
        for attack, enemies in collisions.items():
            for enemy in enemies:
                enemy.decrease_health(attack.damage_value)
    
    def draw(self):
        self.draw_bg()
        self.platforms.draw(self.screen)
        self.player.draw()
        self.enemies.draw()
        self.draw_health_bar()
        self.draw_text_surfaces()
    
    def init_sprites(self):
        self.platforms = pg.sprite.Group()
        self.enemies = enemy.EnemyGroup()
        self.player = Player(100, 100, self.platforms, scroll=0)
        self.create_platforms()
        self.spawn_enemies()
    
    def init_attributes(self):
        self.start_time = time.time()  #initialize starting time
        self.elapsed_time = 0
        
        self.controls = self.get_text_surface(
            "Press 'Escape' to pause", "white", font_size=36
        )
        self.timer = self.get_text_surface(
            f"Level {self.level} Time: {int(self.elapsed_time)}", "white", 
            font_size=36
        )
        self.health_text_surface = self.get_text_surface(
            f"Health: {self.player.health}", "white", font_size=36 
        )
        
    def init_background(self, imgArr):
        self.bg_images = []
        
        if imgArr is not None:
            for i in range(1,6): 
                bg_image = pg.image.load(f"assets/backgrounds/plx-{i}.png").convert_alpha()
                bg_image = pg.transform.smoothscale(bg_image, self.screen.get_size())
                self.bg_images.append(bg_image)
                self.bg_width = self.bg_images[0].get_width()
        
    def init_music(self, music_file):
        # Load background music
        pg.mixer.music.load(os.path.join("assets/music", f"{music_file}"))
        self.volume = 0.5  # Initial volume level (between 0 and 1)
        pg.mixer.music.set_volume(self.volume)
        pg.mixer.music.play(-1)  # Start playing background music on a loop
    
    def create_platforms(self):
        pass # Level-specific behavior
            
    def spawn_enemies(self):
        pass # Level-specific behavior
        
    def timer_update(self):
        self.elapsed_time = time.time() - self.start_time
        self.timer = self.get_text_surface(
            f"Level {self.level} Time: {int(self.elapsed_time)}", "white", 
            font_size=36
        )
    
    def health_update(self):
        self.health_text_surface = self.get_text_surface(
            f"Health: {self.player.health}", "white", font_size=36 
        )
    
    def draw_bg(self):
        for x in range(25):
            speed = 1
            for i in self.bg_images:
                self.screen.blit(i, ((x * self.bg_width) - self.player.scroll * speed, 0))
                speed += 0.2
        
    def draw_health_bar(self):
        # Calculate the width of the health bar based on current health
        health_bar_width = (self.player.health / self.player.max_health) * self.player.health_bar_length
        # Calculate the position of the health bar above the player
        health_bar_x = self.player.rect.x - (self.player.rect.width * (self.player.scale_factor - 1)) / 2
        health_bar_y = self.player.rect.y - 20  # Adjust this value to position the health bar properly
        # Draw the health bar
        pg.draw.rect(self.screen, (255, 0, 0), (health_bar_x, health_bar_y, self.player.health_bar_length, self.player.health_bar_height))
        pg.draw.rect(self.screen, self.player.health_bar_color, (health_bar_x, health_bar_y, health_bar_width, self.player.health_bar_height))

    def draw_text_surfaces(self):
        self.screen.blit(self.controls, (20, 20))
        self.screen.blit(self.health_text_surface, (20, 50))
        self.screen.blit(self.timer, (self.screen.get_width() - 190, 20))
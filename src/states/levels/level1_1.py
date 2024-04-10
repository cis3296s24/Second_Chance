import pygame as pg
import time

from ..state import State
from src.entities.player import Player
from src.objects.platforms import Platform
import src.states.menu.menus as menus
from src.entities.enemies.eyeball import Eyeball  # Import the Eyeball class
from src.entities.enemies.skeleton import Skeleton  # Import the Skeleton class
import src.entities.enemies.enemy as enemy

class Level1_1(State):
    scroll = 0
    def __init__(self):
        super().__init__(None, 1)
        self.platforms = pg.sprite.Group()
        self.enemies = enemy.EnemyGroup()
        self.player = Player(100, 100, self.platforms, self.scroll)
        
        self.controls = pg.font.Font(None, 36).render(
            "Press 'Escape' to pause", True, "white")
        self.start_time = time.time()  #initialize starting time

        # Load background music
        pg.mixer.music.load('assets/music/levelmusic.mp3')
        # Set initial volume
        self.volume = 0.5  # Initial volume level (between 0 and 1)
        pg.mixer.music.set_volume(self.volume)
        pg.mixer.music.play(-1)  # Start playing background music on a loop
        
        self.create_platforms()
        self.spawn_enemies()

    def handle_events(self, events):
        for event in events:
            if event.type != pg.KEYDOWN:
                return
            if event.key == pg.K_ESCAPE:
                self.manager.set_state(menus.PauseMenu, save_prev=True)

    def update(self, events):
        self.player.update()
        self.enemies.update(self.player) # TODO 
        #calculate elapsed time
        self.elapsed_time = time.time() - self.start_time
        
        # Check for collision between player's melee attacks and eyeball
        collisions = pg.sprite.groupcollide(self.player.melee_attacks, self.enemies, False, False)  # Change False to True to remove the melee attack sprite upon collision
        for attack, enemies in collisions.items():
            for enemy in enemies:
                enemy.decrease_health(attack.damage_value)

    def draw(self):
        super().draw_bg()
        self.platforms.draw(self.screen)
        self.player.draw()
        self.enemies.draw()
        self.draw_health_bar()
        self.screen.blit(self.controls, (20, 20))
        self.draw_timer()

        # Draw player's health value
        font = pg.font.Font(None, 36) 
        health_text_surface = font.render(f"Health: {self.player.health}", True, (255, 255, 255))  
        health_text_rect = health_text_surface.get_rect(topleft=(20, 50))  # Adjust position as needed
        self.screen.blit(health_text_surface, health_text_rect)

    def create_platforms(self):
        for i in range(1, 6):
            self.platforms.add(Platform(i * 100, i * 100))

    def spawn_enemies(self):
        self.enemies.add(Eyeball(300, 600, self.platforms, self.scroll))
        self.enemies.add(Skeleton(500, 600, self.platforms, self.scroll))

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

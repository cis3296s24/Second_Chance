import pygame as pg
import time

from ..state import State
from src.entities.player import Player
from src.objects.platforms import Platform
import src.states.menu.menus as menus
from src.entities.enemies.eyeball import Eyeball  # Import the Eyeball class
from src.entities.enemies.skeleton import Skeleton  # Import the Skeleton class

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
        self.spawn_eyeball()  # Call method to spawn an Eyeball
        self.spawn_skeleton()  # Call method to spawn an Eyeball

    def handle_events(self, events):
        for event in events:
            if event.type != pg.KEYDOWN:
                return
            if event.key == pg.K_ESCAPE:
                self.manager.set_state(menus.PauseMenu, save_prev=True)

    def update(self, events):
        self.player.update()
        self.eyeball.update(self.player)  # Update the Eyeball, passing the player object
        self.skeleton.update(self.player) # Update the Skeleton, passing the player object
        #calculate elapsed time
        self.elapsed_time = time.time() - self.start_time
        # Check for collision between player's melee attacks and eyeball
        collisions = pg.sprite.groupcollide(self.player.melee_attacks, self.eyeballs, False, False)  # Change False to True to remove the melee attack sprite upon collision
        for attack, eyeballs in collisions.items():
            for eyeball in eyeballs:
                eyeball.decrease_health(attack.damage_value)

        # Check for collision between player's melee attacks and skeleton
        collisions = pg.sprite.groupcollide(self.player.melee_attacks, self.skeletons, False, False)  # Change False to True to remove the melee attack sprite upon collision
        for attack, skeletons in collisions.items():
            for skeleton in skeletons:
                skeleton.decrease_health(attack.damage_value)

    def draw(self):
        super().draw_bg()
        self.platforms.draw(self.screen)
        self.player.draw()
        self.draw_health_bar()
        self.eyeball.draw() # Draw the Eyeball
        self.skeleton.draw() # Draw the Skeleton
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

    def spawn_eyeball(self):
        # Spawn an Eyeball at coordinates (300, 600)
        self.eyeball = Eyeball(300, 600, self.platforms, self.scroll)
        self.eyeballs = pg.sprite.Group()  # Create a group to hold the Eyeball instances
        self.eyeballs.add(self.eyeball)  # Add the Eyeball instance to the group

    def spawn_skeleton(self):
        # Spawn a Skeleton at coordinates (500, 500)
        self.skeleton = Skeleton(500, 600, self.platforms, self.scroll)
        self.skeletons = pg.sprite.Group()  # Create a group to hold the Eyeball instances
        self.skeletons.add(self.skeleton)  # Add the Eyeball instance to the group

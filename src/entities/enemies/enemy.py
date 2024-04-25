import pygame as pg
import time
import os
import math

class Enemy(pg.sprite.Sprite):
    """Base enemy class.

    Args:
        x (int): x position to spawn at.
        y (int): y position to spawn at.
        platform_group (pygame.sprite.Group): Group of platforms to check
            collision with.
        tiles (list[pygame.Surface]): Group of tiles to check
            collision with.
        image (str): Name of the enemy.
        speed (int): Enemy speed.
        vertical_speed (int): Enemy vertical speed.
        gravity (int): Enemy gravity.
        health (int): Enemy health.
        max_health (int): Enemy max health.
        strength (int): How much damage the enemy does to the player.
    """
    
    def __init__(
        self, 
        x: int, y: int, 
        platform_group: pg.sprite.Group, 
        tiles: list[pg.Surface],
        image: pg.Surface, 
        speed: int, 
        vertical_speed: int, 
        gravity: int,
        health: int,
        max_health: int,
        strength: int,
    ):
        super().__init__()
        self.screen = pg.display.get_surface()
        
        # Load sprite image
        self.image = pg.image.load(
            os.path.join("assets/enemies", f"{image}/{image}.png"), 
        ).convert_alpha()
        self.original_image = self.image  # Store the original image
        # self.rect = self.image.get_rect()
        self.rect = pg.Rect(x,y,50,50)
        self.rect.center = (x,y)
        
        # Define hitbox
        self.hitbox = pg.Rect(x - 10, y - 10, self.rect.width + 20, self.rect.height + 20)  # Adjust hitbox size as needed

        self.platform_group = platform_group
        self.on_ground = False
        self.scale_factor = 2
        self.strength = strength
        self.tile_list = tiles
        
        # Set movement pattern
        self.direction = 1  # 1 for moving right, -1 for moving left
        self.speed = speed
        self.vertical_speed = vertical_speed  # Initial vertical speed for gravity
        self.gravity = gravity  # Adjust this value as needed for gravity effect

        # Define movement boundaries
        self.left_boundary = x - 100  # Adjust this value as needed
        self.right_boundary = x + 100  # Adjust this value as needed

        # Healthbar
        self.health = health  # Initial health value
        self.max_health = max_health  # Maximum health value
        self.health_bar_length = 100  # Length of the health bar
        self.health_bar_height = 10  # Height of the health bar
        self.health_bar_color = (0, 255, 0)  # Green color for the health bar

        # Calculate the position of the health bar
        self.health_bar_offset_x = (self.rect.width - self.health_bar_length) / 2
        self.health_bar_offset_y = self.rect.height / 2 - 30  # 10 pixels above the center of the sprite

        self.invincible = False  # Attribute to track eyeball's invincibility state
        self.invincible_duration = 0.5  # Duration of invincibility frames in seconds
        self.last_hit_time = 0  # Time when the eyeball was last hit

        # Load the sound effect
        self.hit_sound = pg.mixer.Sound(os.path.join("assets/soundeffects", f"{image}hit.mp3"))
 
    def move(self):
        """Adjusts the enemy's position on the screen."""
        
        # Apply gravity
        self.vertical_speed += self.gravity
        self.rect.y += self.vertical_speed
        self.hitbox.y += self.vertical_speed

        # Move enemy left or right based on direction
        self.rect.x += self.speed * self.direction
        self.hitbox.x += self.speed * self.direction

        # Check if Eyeball reaches left or right boundary
        if self.rect.right >= self.right_boundary:
            self.direction = -1  # Change direction to left when reaching right boundary
            self.image = pg.transform.flip(self.original_image, True, False)  # Flip the image horizontally
        elif self.rect.left <= self.left_boundary:
            self.direction = 1  # Change direction to right when reaching left boundary
            self.image = self.original_image  # Restore the original 
        
    def update(self, player):
        """
        Check for conditions that may affect the enemy's position and update
        accordingly through other methods.
        
        Args:
            player (pygame.sprite.Sprite): The player sprite.
        """
        
        # Movement
        self.move()

        # Update rect
        # self.rect.x += scroll  # Adjust for scrolling

        # Keep rect in screen
        # self.rect.x = max(0, min(self.screen.get_width() - self.rect.width, self.rect.x))
        self.rect.y = max(0, min(self.screen.get_height() - self.rect.height, self.rect.y))
                
        # Check for collision with the player
        if self.rect.colliderect(player.rect):
            # If collision occurs, decrease player's health
            player.decrease_health(self.strength)

        self.check_invincibility()

        # Despawn the eyeball if its health reaches 0
        if self.health <= 0:
            self.kill()  # Remove the Eyeball sprite from the group

        self.check_collision()

    def draw(self):
        """Draw the enemy and its health bar onto the screen."""
        # Calculate the position to draw the health bar
        health_bar_x = self.rect.x + self.health_bar_offset_x
        health_bar_y = self.rect.y + self.health_bar_offset_y

        # Draw the health bar
        pg.draw.rect(self.screen, self.health_bar_color, (health_bar_x, health_bar_y, self.health / self.max_health * self.health_bar_length, self.health_bar_height))
        self.screen.blit(self.image, self.rect.topleft)  # Draw the sprite

    def check_collision(self):
        """
        Check collision with tiles or platforms in the level and update
        the enemy's rect accordingly.
        """
        # Create a collision check rectangle that represents the area below the enemy
        collision_check_rect = pg.Rect(self.rect.x, self.rect.y + 1, self.rect.width, 1)

        # Check for collision with tiles below the enemy
        for tile in self.tile_list:
            if self.rect.colliderect(tile.rect):
                # Adjust the enemy's position vertically if moving vertically
                if self.vertical_speed > 0:
                    self.rect.bottom = tile.rect.top
                    self.vertical_speed = 0  # Stop vertical movement
                elif self.vertical_speed < 0:
                    self.rect.top = tile.rect.bottom
                    self.vertical_speed = 0  # Stop vertical movement
                # Check for collision with tiles horizontally if moving horizontally
                elif self.speed > 0:
                    if self.rect.colliderect(tile.rect):
                        self.rect.right = tile.rect.left
                elif self.speed < 0:
                    if self.rect.colliderect(tile.rect):
                        self.rect.left = tile.rect.right
        
    def decrease_health(self, amount):
        """Decreases the enemy's health. 

        Args:
            amount (int): Amount to decrease health by.
        """
        # Check if the eyeball is currently invincible
        if not self.invincible:
            self.health -= amount
            if self.health <= 0:
                self.kill()  # Despawn the eyeball if its health reaches 0
            # Set the eyeball to be invincible and record the time of the hit
            self.invincible = True
            self.last_hit_time = time.time()
            # Play the hit sound effect
            self.hit_sound.play()

    def check_invincibility(self):
        # Check if the eyeball is currently invincible and if the invincibility duration has elapsed
        if self.invincible and time.time() - self.last_hit_time > self.invincible_duration:
            self.invincible = False  # Reset invincibility once the duration has passed

    def increase_health(self, amount):
        self.health += amount
        if self.health > self.max_health:
            self.health = self.max_health


class EnemyGroup(pg.sprite.Group):
    """
    A group class to hold members of the Enemy class used mainly to override
    the pygame.sprite.Group draw() method.
    """
    def draw(self):
        for sprite in self.sprites():
            Enemy.draw(sprite)

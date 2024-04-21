import pygame as pg
import time
import os

class Enemy(pg.sprite.Sprite):
    def __init__(
        self, 
        x, y, 
        platform_group, 
        image, 
        speed, 
        vertical_speed, 
        gravity,
        health,
        max_health,
        strength
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
            self.image = self.original_image  # Restore the original image

        # Check for collision with platforms
        for platform in self.platform_group:
            if self.rect.colliderect(platform.rect):
                # If colliding with a platform, stop falling
                self.vertical_speed = 0
                # Reverse direction if collision occurs
                self.direction *= -1
                if self.direction == -1:
                    self.image = pg.transform.flip(self.original_image, True, False)  # Flip the image horizontally
                else:
                    self.image = self.original_image  # Restore the original image
                break

    def update(self, player, scroll):
        # Movement
        self.move()

        # Update rect
        # self.rect.x += scroll  # Adjust for scrolling

        # Keep rect in screen
        self.rect.x = max(0, min(self.screen.get_width() - self.rect.width, self.rect.x))
        self.rect.y = max(0, min(self.screen.get_height() - self.rect.height, self.rect.y))

        # Check for collision with the player
        if self.rect.colliderect(player.rect):
            # If collision occurs, decrease player's health
            # player.decrease_health(self.strength) # TODO
            pass # TODO remove

        self.check_invincibility()

        # Despawn the eyeball if its health reaches 0
        if self.health <= 0:
            self.kill()  # Remove the Eyeball sprite from the group

    def draw(self):
        # Calculate the position to draw the health bar
        health_bar_x = self.rect.x + self.health_bar_offset_x
        health_bar_y = self.rect.y + self.health_bar_offset_y

        # Draw the health bar
        pg.draw.rect(self.screen, self.health_bar_color, (health_bar_x, health_bar_y, self.health / self.max_health * self.health_bar_length, self.health_bar_height))
        self.screen.blit(self.image, self.rect.topleft)  # Draw the sprite

    def decrease_health(self, amount):
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
    """A group class to override the pygame.sprite.Group draw() method."""
    def draw(self):
        for sprite in self.sprites():
            Enemy.draw(sprite)
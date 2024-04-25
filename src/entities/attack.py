from typing import Any
import pygame as pg
# from src.entities.player import Player as player
from src.entities.enemies.enemy import Enemy as enemy

arrows_group = pg.sprite.Group()
class MeleeAttack(pg.sprite.Sprite):
    """Sprite to represent a melee attack performed by the player.

    Args:
        x (int): x position of the attack,
        y (int): y position of the attack.
        player_direction (str): Direction that the player is currently
            facing. 
        damage_value (int, optional): Amount of damage that this attack does. 
            Defaults to 25.
    """
    
    def __init__(self, x, y, player_direction, damage_value=25):
        super().__init__()
        self.screen = pg.display.get_surface()
        self.attack_animation = [self.animationopen("attack1"), self.animationopen("attack2"), self.animationopen("attack3"), self.animationopen("attack4")]
        self.flipped_attack_animation = [pg.transform.flip(image, True, False) for image in self.attack_animation]  # Flip the animation frames
        self.current_frame = 0
        self.image = self.flipped_attack_animation[self.current_frame] if player_direction == "left" else self.attack_animation[self.current_frame]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.animation_speed = 6
        self.animation_timer = 0
        self.player_direction = player_direction
        self.damage_value = damage_value  # Set the damage value for the melee attack

    def animationopen(self, imageName):
        imageLoad = pg.image.load("assets/attackanimation/" + imageName + ".png").convert_alpha()
        return imageLoad

    def update(self):
        """Animates the attack."""
                
        # Animate the attack
        self.animation_timer += 1
        if self.animation_timer >= self.animation_speed:
            self.current_frame += 1
            if self.current_frame >= len(self.attack_animation):
                self.kill()  # Kill the sprite when the animation ends
            else:
                self.image = self.flipped_attack_animation[self.current_frame] if self.player_direction == "left" else self.attack_animation[self.current_frame]  # Use flipped animation if facing left
                self.animation_timer = 0

    def draw(self):
        """Draws the attack onto the screen."""
        
        self.screen.blit(self.image, self.rect.topleft)

class RangeAttack(pg.sprite.Sprite):
    """Sprite to represent a range attack performed by the player.

    Args:
        x (int): x position of the attack,
        y (int): y position of the attack.
        player_direction (str): Direction that the player is currently
            facing. 
        damage_value (int, optional): Amount of damage that this attack does. 
            Defaults to 25.
    """
    
    def __init__(self, x, y, player_direction, damage_value=25):
        super().__init__()
        self.screen = pg.display.get_surface()
        self.damage_value = damage_value
        self.image = pg.image.load(open("assets/enemies/archer/arrow_R.png"))
        self.rect = self.image.get_rect()
        self.direction = 1 if player_direction == "right" else -1
        self.speed = 9
        self.rect.center = (x, y)

    def update(self):
        """Updates the position of the attack."""
        self.rect.x += (self.direction * self.speed)
                
    def draw(self):
        """Draws the attack onto the screen."""
        self.screen.blit(self.image,self.rect.topleft)

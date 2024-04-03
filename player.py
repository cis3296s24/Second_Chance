import pygame as pg
import math
from platforms import Platform

class Player(pg.sprite.Sprite):

    
    def __init__(self, x, y, width, height, color, platform_group):
        super().__init__()
        self.screen = pg.display.get_surface()
        self.image = pg.Surface((width, height))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.color = color
        self.platform_group = platform_group
        self.on_ground = False
        self.scale_factor = 2
        
        #Path for character image
        self.character_image = pg.image.load(open("images/character/stand.png"))
        
        self.character_image = pg.transform.scale(self.character_image, (self.rect.width * self.scale_factor, self.rect.height * self.scale_factor))
        
        self.font = pg.font.Font(None, 36) # TODO
        
        self.speed = 5
        self.gravity = 0.5
        self.vertical_velocity = 0
        self.jump_strength = -15

    def move(self):
        #move as specified
        keys = pg.key.get_pressed()
        
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.rect.x -= self.speed
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.rect.x += self.speed

    def jump(self):
        #check if the character is on the ground        
        if self.on_ground:
            self.vertical_velocity = self.jump_strength
            self.on_ground = False
        
    def check_collision(self):
        # Check if rect (after being updated) collides with platform
        player_rect_after = pg.Rect(
            self.rect.x, self.rect.y + math.ceil(self.vertical_velocity), 
            self.rect.width, self.rect.height
        )
        for platform in self.platform_group:
            if platform.rect.colliderect(player_rect_after):
                if self.vertical_velocity > 0: # if currently falling
                    self.vertical_velocity = 0 # stop falling
                    self.rect.bottom = platform.rect.top
                    self.on_ground = True

    def update(self):
        #get keys that are pressed
        keys = pg.key.get_pressed()        
        
        # Apply gravity
        self.vertical_velocity += self.gravity
        
        # If falling, we're not on ground
        if self.vertical_velocity > 0:
            self.on_ground = False
        
        # Check collision with ground
        if self.rect.bottom >= self.screen.get_height():
            self.rect.bottom = self.screen.get_height()
            self.on_ground = True
            self.vertical_velocity = 0
            
        # Check collision with platforms
        self.check_collision()
            
        # Movement
        self.move()

        # Jumping
        if keys[pg.K_SPACE] or keys[pg.K_UP] or keys[pg.K_w]:
            self.jump()
        
        # Update rect
        self.rect.y += self.vertical_velocity
        
        #keep rect in screen
        self.rect.x = max(0, min(self.screen.get_width() - self.rect.width, self.rect.x))
        self.rect.y = max(0, min(self.screen.get_height() - self.rect.height, self.rect.y))
        
        # Display player info for debugging purposes
        # self.debug()
        
        
    def draw(self):
        image_x = self.rect.x - (self.rect.width * (self.scale_factor - 1)) / 2
        image_y = self.rect.y - (self.rect.height * (self.scale_factor - 1)) / 2
        self.screen.blit(self.character_image, (image_x, image_y))

    def debug(self):
        text = f"""
        Grounded: {self.on_ground} 
        | Y: {self.rect.y} 
        | Vel: {self.vertical_velocity}
        | {self.rect.bottom}, {self.screen.get_height()}"""
        text_surface = self.font.render(text, True, "red")
        self.screen.blit(text_surface, (0,20))
    
    def characteropen(imageName):
        return open("images/character/" + imageName)
        
        
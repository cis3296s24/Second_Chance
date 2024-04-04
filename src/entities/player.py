import pygame as pg
import math
from src.objects.platforms import Platform

class Player(pg.sprite.Sprite):
  
    def characteropen(imageName):
        imageLoad = pg.image.load(open("assets/characters/" + imageName + ".png")) 
        return imageLoad
    animationRight = [characteropen("R1"),characteropen("R2"),characteropen("R3"),characteropen("R4"),characteropen("R5"),characteropen("R6"),characteropen("R7"),characteropen("R8"),characteropen("R9")]
    animationLeft = [characteropen("L1"),characteropen("L2"),characteropen("L3"),characteropen("L4"),characteropen("L5"),characteropen("L6"),characteropen("L7"),characteropen("L8"),characteropen("L9")]
    
    def __init__(self, x, y, platform_group, scroll):
        super().__init__()
        self.screen = pg.display.get_surface()
        self.image = pg.Surface((50, 50))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.platform_group = platform_group
        self.on_ground = False
        self.scale_factor = 2
        self.scroll = 0
        #Path for character image
        self.character_image = pg.image.load(open("assets/characters/stand.png"))
        
        self.character_image = pg.transform.scale(self.character_image, (self.rect.width * self.scale_factor, self.rect.height * self.scale_factor))
        
        self.font = pg.font.Font(None, 36) # TODO
        
        self.speed = 2
        self.gravity = 0.5
        self.vertical_velocity = 0
        self.jump_strength = -15

    walkcount = 0
    isRight = False
    isLeft = False
    prevPress = ""
    def move(self):
        #move as specified
        keys = pg.key.get_pressed()

#         check player is facing right or left
        if (keys[pg.K_LEFT] or keys[pg.K_a]) and self.scroll > 0:
            self.rect.x -= self.speed
            self.scroll -= 3
            self.isRight = False
            self.isLeft = True
            self.prevPress = "left"
            for platform in self.platform_group:
                platform.rect.x += 3  # Move platforms with player
        elif (keys[pg.K_RIGHT] or keys[pg.K_d]) and self.scroll < 5000:
            self.rect.x += self.speed
            self.scroll += 3
            self.isRight = True
            self.isLeft = False
            self.prevPress = "right"
            for platform in self.platform_group:
                platform.rect.x -= 3  # Move platforms with player
        else:
            self.isLeft = False
            self.isRight = False
            self.walkcount = 0
            
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

        if self.isRight:
            self.character_image = self.animationRight[self.walkcount//3]
            self.character_image = pg.transform.scale(self.character_image, (self.rect.width * self.scale_factor, self.rect.height * self.scale_factor))
            self.screen.blit(self.character_image,(image_x,image_y))
            self.walkcount += 1
            
        elif self.isLeft:
            self.character_image = self.animationLeft[self.walkcount//3]
            self.character_image = pg.transform.scale(self.character_image, (self.rect.width * self.scale_factor, self.rect.height * self.scale_factor))
            self.screen.blit(self.character_image,(image_x,image_y))
            self.walkcount += 1 

        else:
            if (self.prevPress == "left"):
                self.character_image = pg.image.load(open("assets/characters/stand_L.png"))
            else:
                self.character_image = pg.image.load(open("assets/characters/stand.png"))
            self.character_image = pg.transform.scale(self.character_image, (self.rect.width * self.scale_factor, self.rect.height * self.scale_factor))
            self.screen.blit(self.character_image,(image_x,image_y))

        if self.walkcount + 1 >= 27 :
            self.walkcount = 0

    def debug(self):
        text = f"""
        Grounded: {self.on_ground} 
        | Y: {self.rect.y} 
        | Vel: {self.vertical_velocity}
        | {self.rect.bottom}, {self.screen.get_height()}"""
        text_surface = self.font.render(text, True, "red")
        self.screen.blit(text_surface, (0,20))
        
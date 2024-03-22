import pygame as pg

class Player(pg.sprite.Sprite):
    def __init__(self, x, y, width, height, speed, color):
        super().__init__()
        self.screen = pg.display.get_surface()
        self.image = pg.Surface((width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.color = color
        
        self.speed = speed
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
        if self.rect.y == self.screen.get_height() - self.rect.height:  
            self.vertical_velocity = self.jump_strength
        
    def apply_gravity(self):
        # Apply gravity
        self.vertical_velocity += self.gravity
        self.rect.y += self.vertical_velocity

    def update(self):
        #get keys that are pressed
        keys = pg.key.get_pressed()
        
        self.move()
        
        if keys[pg.K_SPACE] or keys[pg.K_UP] or keys[pg.K_w]:
            self.jump()
            
        self.apply_gravity()
        
        #keep rect in screen
        self.rect.x = max(0, min(self.screen.get_width() - self.rect.width, self.rect.x))
        self.rect.y = max(0, min(self.screen.get_height() - self.rect.height, self.rect.y))

    def draw(self):
        self.screen.fill(self.color, self.rect)

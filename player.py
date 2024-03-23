import pygame as pg

class Player(pg.sprite.Sprite):
    def __init__(self, x, y, width, height, speed, color, platform_group):
        super().__init__()
        self.screen = pg.display.get_surface()
        self.image = pg.Surface((width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.color = color
        self.platform_group = platform_group
        self.on_ground = False
        
        self.font = pg.font.Font(None, 36) # TODO
        
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
        
        # TODO remove
        if keys[pg.K_w]:
            self.rect.y -= self.speed
        if keys[pg.K_s]:
            self.rect.y += self.speed

    def jump(self):
        #check if the character is on the ground        
        if self.on_ground:
            self.vertical_velocity = self.jump_strength
        
    def apply_gravity(self):
        # Apply gravity
        self.vertical_velocity += self.gravity
        self.rect.y += self.vertical_velocity

    def check_collision(self):
        for platform in self.platform_group:
            # self.on_ground = pg.sprite.collide_rect(self, platform)
            if self.on_ground and self.rect.bottom < platform.rect.centery:
                if self.vertical_velocity > 0: # falling
                    self.apply_gravity()
                else:
                    self.rect.bottom = platform.rect.top

    def update(self):
        #get keys that are pressed
        keys = pg.key.get_pressed()
        
        self.move()
        
        if keys[pg.K_SPACE] or keys[pg.K_UP] or keys[pg.K_w]:
            self.jump()
        
        self.on_ground = self.rect.bottom + 1 > self.screen.get_height()
        
        if not self.on_ground:
            self.apply_gravity()
        
        self.check_collision()
        
        #keep rect in screen
        self.rect.x = max(0, min(self.screen.get_width() - self.rect.width, self.rect.x))
        self.rect.y = max(0, min(self.screen.get_height() - self.rect.height, self.rect.y))
        
        self.debug()

    def draw(self):
        self.screen.fill(self.color, self.rect)

    def debug(self):
        text = f"""
        Grounded: {self.on_ground} 
        | Y: {self.rect.y} 
        | {self.vertical_velocity}
        | {self.rect.bottom}, {self.screen.get_height()}"""
        text_surface = self.font.render(text, True, "red")
        self.screen.blit(text_surface, (0,20))
        
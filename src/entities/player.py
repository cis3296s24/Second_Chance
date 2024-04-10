import pygame as pg
import math
import time
from src.objects.platforms import Platform
from src.entities.attack import MeleeAttack

from src.entities.green_button import GreenButton

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

        self.invincible = False  # Attribute to track player's invincibility state
        self.invincible_duration = 2  # Duration of invincibility frames in seconds
        self.last_hit_time = 0  # Time when the player was last hit

        self.melee_attacks = pg.sprite.Group()  # Group for managing melee attack instances
        self.attack_initiated = False
        self.prev_x = x  # Store the initial x-coordinate as previous x-coordinate
        
        #Path for character image
        self.character_image = pg.image.load(open("assets/characters/stand.png"))

        # Load the sound effect
        self.hit_sound = pg.mixer.Sound("assets/soundeffects/playerhit.mp3")

        # Load the sound effect
        self.melee_attack_sound = pg.mixer.Sound("assets/soundeffects/meleeattack.mp3")
        
        self.character_image = pg.transform.scale(self.character_image, (self.rect.width * self.scale_factor, self.rect.height * self.scale_factor))
        
        self.font = pg.font.Font(None, 36) # TODO
        
        self.speed = 2
        self.gravity = 0.5
        self.vertical_velocity = 0
        self.jump_strength = -15

        # Healthbar
        self.health = 100  # Initial health value
        self.max_health = 100  # Maximum health value
        self.health_bar_length = 100  # Length of the health bar
        self.health_bar_height = 10  # Height of the health bar
        self.health_bar_color = (0, 255, 0)  # Green color for the health bar
        
        # Define hitbox
        self.hitbox = pg.Rect(x, y, self.rect.width, self.rect.height)

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
        # Check if hitbox (after being updated) collides with platform
        hitbox_after = pg.Rect(
            self.rect.x, self.rect.y + math.ceil(self.vertical_velocity), 
            self.rect.width, self.rect.height
        )
        for platform in self.platform_group:
            if platform.rect.colliderect(hitbox_after):
                if self.vertical_velocity > 0: # if currently falling
                    self.vertical_velocity = 0 # stop falling
                    self.rect.bottom = platform.rect.top
                    self.on_ground = True

    def update(self):
        # Get keys that are pressed
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
        
        # Update hitbox
        self.hitbox.y += self.vertical_velocity

        self.check_invincibility()
        
        # Keep rect in screen
        self.rect.x = max(0, min(self.screen.get_width() - self.rect.width, self.rect.x))
        self.rect.y = max(0, min(self.screen.get_height() - self.rect.height, self.rect.y))

        # Detect left mouse button click event
        mouse_buttons = pg.mouse.get_pressed()

        q_pressed = keys[pg.K_q] #Q and click both attack
        
        # Update facing direction based on current and previous x-coordinates
        if self.rect.x > self.prev_x:
            self.isRight = True
            self.isLeft = False
        elif self.rect.x < self.prev_x:
            self.isRight = False
            self.isLeft = True

        # Update previous x-coordinate for the next cycle
        self.prev_x = self.rect.x

        # Determine player direction for melee attack
        if self.isRight:
            player_direction = "right"
        elif self.isLeft:
            player_direction = "left"
        else:
            # Use previous facing direction if not moving
            if self.prevPress == "left":
                player_direction = "left"
            else:
                player_direction = "right"
                
        # Create a melee attack instance at the player's position
        if player_direction == "right":
            melee_attack = MeleeAttack(self.rect.centerx + 20, self.rect.centery, player_direction, damage_value=25)
        else:
            melee_attack = MeleeAttack(self.rect.centerx - 20, self.rect.centery, player_direction, damage_value=25)
            
        # Check for initiating attack
        if (mouse_buttons[0] or q_pressed) and not self.attack_initiated:
            self.melee_attack_sound.play()
            self.melee_attacks.add(melee_attack)
            self.attack_initiated = True
            
        if not (mouse_buttons[0] or q_pressed):
            self.attack_initiated = False

        self.melee_attacks.update()

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

        # Draw melee attacks
        self.melee_attacks.draw(self.screen)

    def decrease_health(self, amount):
        # Check if the player is currently invincible
        if not self.invincible:
            self.health -= amount

            # Prevent the player's HP from being reduced below 0
            if self.health < 0:
                self.health = 0

            # If the player's HP is reduced to 0, the demo second chance game pops up
            # Once the second chance game is completed, the player's HP is restored to 100
            if self.health == 0:
                #have the second chance at this point
                GREEN = (0, 255, 0)
                demo_chance = GreenButton(self.screen, GREEN, 300, 250, 200, 100)
                demo_chance.display()
                self.health = 100

            # Set the player to be invincible and record the time of the hit
            self.invincible = True
            self.last_hit_time = time.time()
            # Play the hit sound effect
            self.hit_sound.play()

    def check_invincibility(self):
        # Check if the player is currently invincible and if the invincibility duration has elapsed
        if self.invincible and time.time() - self.last_hit_time > self.invincible_duration:
            self.invincible = False  # Reset invincibility once the duration has passed

    def increase_health(self, amount):
        self.health += amount
        if self.health > self.max_health:
            self.health = self.max_health

    def debug(self):
        text = f"""
        Grounded: {self.on_ground} 
        | Y: {self.rect.y} 
        | Vel: {self.vertical_velocity}
        | {self.rect.bottom}, {self.screen.get_height()}"""
        text_surface = self.font.render(text, True, "red")
        self.screen.blit(text_surface, (0,20))

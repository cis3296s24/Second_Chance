import pygame as pg
import math
import time

from src.entities.attack import MeleeAttack
from src.entities.attack import RangeAttack
from src.constants import *
from src.utils.timer import Timer

class Player(pg.sprite.Sprite):

    def __init__(self, x, y, platform_group, portal_group, obstacle_list):

        super().__init__()
        
        self.screen = pg.display.get_surface()
        self.size = (100, 100)
        self.animation = [
            pg.transform.scale(pg.image.load(f"assets/characters/R{i}.png"), self.size).convert_alpha() 
                for i in range(1, 10)]
        
        self.image = pg.image.load(f"assets/characters/stand.png") 
        self.image = pg.transform.scale(self.image, (self.image.get_width() * 2, self.image.get_height() * 2))  # Scale the sprite
        self.idle = self.image
        self.rect = self.image.get_rect()  
        
        # Set the rect for the sprite
        self.rect.center = (x, y)
        self.rect.width //= 2
        self.rect.height //= 2
        self.sprite_x = 0
        self.sprite_y = 0 
        
        # Player actions and state
        self.is_moving = False
        self.on_ground = False
        self.is_jumping = False
        self.direction = "right"
        
        # Player inputs
        self.up_press = False
        self.left_press = False
        self.right_press = False
        self.movement_pressed = False
        self.melee_pressed = False
        self.ranged_pressed = False
        
        # Animation variables
        self.index = 0
        self.counter = 0
        self.walk_cooldown = 3
        self.scroll = 0
        
        self.platform_group = platform_group
        self.portal_group = portal_group
        self.obstacle_list = obstacle_list
        self.scale_factor = 2

        self.invincible = False  # Attribute to track player's invincibility state
        self.invincible_duration = 1.5  # Duration of invincibility frames in seconds
        self.last_hit_time = 0  # Time when the player was last hit
        
        self.timer = Timer(start=True)
        self.last_health_increase_time = 0
        self.health_duration = 3 # How often to increase HP in seconds
        self.health_increase_amount = 10

        self.melee_attacks = pg.sprite.Group()  # Group for managing melee attack instances
        self.range_attacks = pg.sprite.Group()

        self.attack_initiated = False
        self.rangeAttack_initiated = False

        self.prev_x = x  # Store the initial x-coordinate as previous x-coordinate

        self.last_ranged_attack_time = 0  # Initialize with 0
        self.ranged_attack_cooldown = 3  # Cooldown duration for the ranged attack in seconds

        self.ranged_attack_count = 0  # Initialize the counter for ranged attacks
        self.ranged_attack_max = 10 # Maximum number of ranged attack uses the player has

        # Load the sound effects
        self.hit_sound = pg.mixer.Sound("assets/soundeffects/playerhit.mp3")
        self.melee_attack_sound = pg.mixer.Sound("assets/soundeffects/meleeattack.mp3")
        self.ranged_attack_sound = pg.mixer.Sound("assets/soundeffects/rangedattack.mp3")
        
        self.font = pg.font.Font(None, 20) # TODO
        
        self.speed = 2.5
        self.gravity = 0.5
        self.vel_y = 0
        self.jump_strength = -15

        # Healthbar
        self.health = 100  # Initial health value
        self.max_health = 100  # Maximum health value
        self.health_bar_length = 100  # Length of the health bar
        self.health_bar_height = 10  # Height of the health bar
        self.health_bar_color = (0, 255, 0)  # Green color for the health bar
        
        # Define hitbox
        self.hitbox = pg.Rect(x, y, self.rect.width, self.rect.height)

    def update(self):
        self.dx = 0
        self.dy = 0
        self.scroll = 0
        
        # Set variables depending on input
        self.input()
        
        # Move depending on variables set
        self.move()
                
        # Get current time to check for timed events
        current_time = self.timer.get_time(ms=True)    

        # Apply gravity
        self.vel_y += self.gravity
        self.dy += self.vel_y
        
        self.handle_animation()
        
        # If falling, we're not on ground
        if self.vel_y > 0:
            self.on_ground = False
        
        # Check collision with platforms
        self.check_collision()
        
        # Check collision with ground
        if self.rect.bottom >= self.screen.get_height():
            self.rect.bottom = self.screen.get_height()
            self.on_ground = True
            self.vel_y = 0
            
        # Jumping
        if self.on_ground and self.is_jumping:
            self.jump()
        
        # Update rect
        self.rect.x += self.dx
        self.rect.y += self.dy
        
        # Update hitbox
        self.hitbox.y += self.vel_y

        self.check_invincibility()
        
        # Increase HP after a certain amount of time has passed
        if current_time - self.last_health_increase_time > self.health_duration:
            self.increase_health(self.health_increase_amount)
            self.last_health_increase_time = current_time
        
        # Keep rect in screen
        self.rect.x = max(0, min(self.screen.get_width() - self.rect.width, self.rect.x))
        self.rect.y = max(0, min(self.screen.get_height() - self.rect.height, self.rect.y))
        
        # To center sprite in rect
        self.sprite_x = self.rect.x + (self.rect.width - self.image.get_width()) // 2
        self.sprite_y = self.rect.y + (self.rect.height - self.image.get_height()) // 2

        # Update previous x-coordinate for the next cycle
        self.prev_x = self.rect.x
                
        # Create a melee attack instance at the player's position
        if self.direction == "right":
            melee_attack = MeleeAttack(self.rect.centerx + 20, self.rect.centery, self.direction, damage_value=25)
            range_attack = RangeAttack(self.rect.centerx + 10,self.rect.centery,self.direction,damage_value= 25)
        else:
            melee_attack = MeleeAttack(self.rect.centerx - 20, self.rect.centery, self.direction, damage_value=25)
            range_attack = RangeAttack(self.rect.centerx - 10,self.rect.centery,self.direction,damage_value= 25)
            
        # Check for initiating attack
        if self.melee_pressed and not self.attack_initiated:
            self.melee_attack_sound.play()
            self.melee_attacks.add(melee_attack)
            self.attack_initiated = True
            
        if not self.melee_pressed:
            self.attack_initiated = False

        self.melee_attacks.update()

        # Get current time
        current_time = time.time()

        # Check if enough time has passed since the last ranged attack
        if (current_time - self.last_ranged_attack_time >= self.ranged_attack_cooldown) or (self.last_ranged_attack_time == 0):
            # Allow ranged attack initiation if the count is less than the maximum
            if self.ranged_pressed and not self.rangeAttack_initiated and self.ranged_attack_count < self.ranged_attack_max:
                self.ranged_attack_sound.play()
                self.range_attacks.add(range_attack)
                self.rangeAttack_initiated = True
                # Increment the ranged attack count
                self.ranged_attack_count += 1
                # Update the time of the last ranged attack
                self.last_ranged_attack_time = current_time
        
        if not self.ranged_pressed:
            self.rangeAttack_initiated = False
        
        self.range_attacks.update()

        # Scroll by the amoaunt moved horizontally
        return self.scroll

    def input(self):
        keys = pg.key.get_pressed()
        mouse_buttons = pg.mouse.get_pressed()
        
        self.melee_pressed = keys[pg.K_q] or mouse_buttons[0] # Q and left click for melee attack
        self.ranged_pressed = keys[pg.K_e] or mouse_buttons[2] # E and right click for ranged attack 
        
        self.up_press = keys[pg.K_SPACE] or keys[pg.K_UP] or keys[pg.K_w]
        self.left_press = keys[pg.K_LEFT] or keys[pg.K_a]
        self.right_press = keys[pg.K_RIGHT] or keys[pg.K_d]
        self.movement_pressed = self.left_press or self.right_press
        
        self.is_jumping = self.up_press
        
        if self.movement_pressed:
            self.is_moving = True
            if self.left_press:     
                self.direction = "left"
            if self.right_press:
                self.direction = "right"
        else:
            self.is_moving = False

    def move(self):
        if self.movement_pressed:
            self.counter += 1
            if self.left_press:     
                self.dx -= self.speed
                self.scroll += self.speed
            if self.right_press:
                self.dx += self.speed
                self.scroll -= self.speed
        else:
            self.dx = 0
            self.scroll = 0
            
        if self.rect.x + self.dx > SCREEN_WIDTH - SCROLL_THRESH:
            self.rect.x = SCREEN_WIDTH - SCROLL_THRESH
            self.scroll += self.speed

    def jump(self):
        self.vel_y = self.jump_strength
        self.dy += self.vel_y
        self.on_ground = False

    def check_collision(self):
        # Check if hitbox (after being updated) collides with platform
        hitbox_after = pg.Rect(
            self.rect.x, self.rect.y + math.ceil(self.vel_y), 
            self.rect.width, self.rect.height
        )
        for platform in self.platform_group:
            if platform.rect.colliderect(hitbox_after):
                if self.vel_y > 0: # if currently falling
                    self.vel_y = 0 # stop falling
                    self.rect.bottom = platform.rect.top
                    self.on_ground = True

        # for tile in self.obstacle_list:
        #     if tile[1].colliderect(hitbox_after):
        #         if self.vel_y > 0: # if currently falling
        #             self.vel_y = 0 # stop falling
        #             self.rect.bottom = tile[1].top
        #             self.on_ground = True
        
        x_check = pg.Rect(self.rect.x + self.dx, self.dy, self.rect.width, self.rect.height)
        y_check = pg.Rect(self.rect.x, self.rect.y + math.ceil(self.dy),
        self.rect.width, self.rect.height)
        
        for tile in self.obstacle_list:
            # Horizontal collision
            if tile.rect.colliderect(x_check):
                self.dx = 0
                self.scroll = 0
            # Vertical collision
            if tile.rect.colliderect(y_check):
                if self.vel_y >= 0: # If falling
                    self.dy = tile.rect.top - self.rect.bottom
                    self.vel_y = 0
                    self.on_ground = True
                    self.is_moving = False

    def handle_animation(self):
        if self.counter > self.walk_cooldown:
            self.counter = 0	
            self.index += 1
            if self.index >= len(self.animation):
                self.index = 0
                
        animation = self.animation[self.index]

        if not self.is_moving:
            self.image = self.idle
        else:
            self.image = animation
            
        flip = self.direction == "left"
        self.image = pg.transform.flip(self.image, flip, False)    
        
    def draw(self):
        self.screen.blit(self.image, (self.sprite_x, self.sprite_y))
        self.melee_attacks.draw(self.screen) 

        # Draw melee attacks
        self.melee_attacks.draw(self.screen)
        self.range_attacks.draw(self.screen)

        # Draw the remaining ranged attacks count
        self.draw_range_attack_count()

    def decrease_health(self, amount):
        # Check if the player is currently invincible
        if not self.invincible:
            self.health -= amount

            # Prevent the player's HP from being reduced below 0
            if self.health < 0:
                self.health = 0

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

    def draw_range_attack_count(self):
        # Render the text for displaying the remaining ranged attacks count
        text_count = f"{10 - self.ranged_attack_count}"
        text_surface_count = self.font.render(text_count, True, (255, 255, 255))  # White color text
        
        # Render the static label "Arrows Left:"
        text_label = "Arrows Left: "
        text_surface_label = self.font.render(text_label, True, (255, 255, 255))  # White color text

        # Get the width of the label
        label_width = text_surface_label.get_width()

        # Calculate the position of the label (left-aligned)
        label_x = 19  # Adjust this value as needed
        label_y = 80  # Adjust this value as needed

        # Calculate the position of the count (right-aligned)
        count_x = label_x + label_width  # Position the count to the right of the label
        count_y = label_y  # Align the count vertically with the label

        # Blit the label onto the screen
        self.screen.blit(text_surface_label, (label_x, label_y))

        # Blit the count onto the screen
        self.screen.blit(text_surface_count, (count_x, count_y))

    def debug(self):
        text = \
      	f"""
     	Grounded: {self.on_ground}
		| (dx, dy) : {(self.dx, self.dy)}
        | (rect.x, rect.y): {(self.rect.x, self.rect.y)} 
        | Vel: {self.vel_y}
        """
        text_surface = self.font.render(text, True, "red")
        pg.draw.rect(self.screen, (255, 255, 255), self.rect, 2)
        self.screen.blit(text_surface, (0, 100))

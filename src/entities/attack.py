import pygame as pg

class MeleeAttack(pg.sprite.Sprite):
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
        self.screen.blit(self.image, self.rect.topleft)
import pygame
import sys
from player import Player
from platforms import Platform

pygame.init()

#setup screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

#color
RED = (255, 0, 0)

#character properties
rect_width = 50
rect_height = 50
rect_x = (screen_width - rect_width) // 2
rect_y = (screen_height - rect_height) // 2
rect_speed = 5
player = Player(rect_x, rect_y, rect_width, rect_height, rect_speed, RED)

# Platforms
platform_group = pygame.sprite.Group()
platform_group.add(
    Platform(100, 100),
    Platform(200, 200),
    Platform(300, 300),
    Platform(400, 400),
    Platform(500, 500)
)

#gravity properties
gravity = 0.5
vertical_velocity = 0
jump_strength = -15  #negative value to move upwards

clock = pygame.time.Clock()

#main game loop
running = True
while running:
    screen.fill((0, 0, 0))  #black backgrund

    #handle events, this will contain more in future
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    player.update()
    
    for platform in platform_group:
        if pygame.sprite.collide_rect(player, platform):
            player.rect.bottom = platform.rect.top

    platform_group.draw(screen)
    player.draw()

    pygame.display.flip()
    clock.tick(60)

#quit/exit
pygame.quit()
sys.exit()

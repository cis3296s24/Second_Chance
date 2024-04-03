import pygame
import sys
from player import Player
from platforms import Platform

pygame.init()

#setup screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Second Chance")
# try:
#     bg = pygame.image.load(open("images/back.png"))

# except:
#     print("file not found")

#define game variables
scroll = 0


#color
RED = (255, 0, 0)

# Platforms
platform_group = pygame.sprite.Group()
platform_group.add(
    Platform(100, 100),
    Platform(200, 200),
    Platform(300, 300),
    Platform(400, 400),
    Platform(500, 500)
)

#character properties
rect_width = 50
rect_height = 50
rect_x = (screen_width - rect_width) // 2
rect_y = (screen_height - rect_height) // 2
rect_speed = 5
player = Player(rect_x, rect_y, rect_width, rect_height, RED, platform_group, scroll)


#background
bg_images = []
for i in range(1,6): 
    bg_image = pygame.image.load(f"images/plx-{i}.png").convert_alpha()
    bg_image = pygame.transform.smoothscale(bg_image, screen.get_size())
    bg_images.append(bg_image)

bg_width = bg_images[0].get_width()
bg_height = bg_images[0].get_height()


def draw_bg():
    for x in range(25):
        speed = 1
        for i in bg_images:
           screen.blit(i, ((x * bg_width) - player.scroll * speed, 0))
           speed += 0.2


#gravity properties
gravity = 0.5
vertical_velocity = 0
jump_strength = -15  #negative value to move upwards

clock = pygame.time.Clock()

#main game loop
running = True
while running:
    clock.tick(60)
    draw_bg()

    #handle events, this will contain more in future
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    player.update()

    platform_group.draw(screen)
    player.draw()

    pygame.display.flip()

#quit/exit
pygame.quit()
sys.exit()

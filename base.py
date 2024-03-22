import pygame
import sys


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

clock = pygame.time.Clock()

#main game loop
running = True
while running:
    screen.fill((0, 0, 0))  #black backgrund

    #handle events, this will contain more in future
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #get keys that are pressed
    keys = pygame.key.get_pressed()

    #move as specified
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        rect_x -= rect_speed
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        rect_x += rect_speed
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        rect_y -= rect_speed
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        rect_y += rect_speed

    #keep rect in screen
    rect_x = max(0, min(screen_width - rect_width, rect_x))
    rect_y = max(0, min(screen_height - rect_height, rect_y))

    #draw rect (character in future)
    pygame.draw.rect(screen, RED, (rect_x, rect_y, rect_width, rect_height))

    pygame.display.flip()
    clock.tick(60)

#quit/exit
pygame.quit()
sys.exit()
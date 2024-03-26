import pygame
import sys


pygame.init()

#setup screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))


#color
RED = (255, 0, 0)

image = pygame.image.load('character.png')  # Replace "your_image_path.png" with the path to your image

#character properties
rect_width = 50
rect_height = 50
rect_x = (screen_width - rect_width) // 2
rect_y = (screen_height - rect_height) // 2
rect_speed = 5

scale_factor = 2
image = pygame.transform.scale(image, (rect_width * scale_factor, rect_height * scale_factor))  # Scale image to match rectangle size

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

    #get keys that are pressed
    keys = pygame.key.get_pressed()

    #move as specified
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        rect_x -= rect_speed
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        rect_x += rect_speed

    #jump
    if keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]:
        if rect_y == screen_height - rect_height:  #check if the character is on the ground
            vertical_velocity = jump_strength

    # Apply gravity
    vertical_velocity += gravity
    rect_y += vertical_velocity

    #keep rect in screen
    rect_x = max(0, min(screen_width - rect_width, rect_x))
    rect_y = max(0, min(screen_height - rect_height, rect_y))

    #draw rect (character in future)
    pygame.draw.rect(screen, RED, (rect_x, rect_y, rect_width, rect_height))
    
    image_x = rect_x - (rect_width * (scale_factor - 1)) / 2
    image_y = rect_y - (rect_height * (scale_factor - 1)) / 2
    
    screen.blit(image, (image_x, image_y))

    pygame.display.flip()
    clock.tick(60)

#quit/exit
pygame.quit()
sys.exit()

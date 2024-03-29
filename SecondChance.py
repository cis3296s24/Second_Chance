import pygame
import pygame_menu
import sys
from src.entities.player import Player
from src.objects.platforms import Platform

pygame.init()

#setup screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

#color
RED = (255, 0, 0)

def main_menu():
    # Create menu
    menu = pygame_menu.Menu('Second Chance', screen_width, screen_height, theme=pygame_menu.themes.THEME_BLUE)

    # Add buttons to the menu
    menu.add.button('Start Game', game_loop)
    menu.add.button("Instructions")
    menu.add.button("Leaderboard")
    menu.add.button("Options")
    menu.add.button('Quit', pygame_menu.events.EXIT)

    # Run menu
    menu.mainloop(screen)

def game_loop():
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
    player = Player(rect_x, rect_y, rect_width, rect_height, RED, platform_group)

    clock = pygame.time.Clock()

    try:
        bg = pygame.image.load(open("assets/backgrounds/back.png"))
    except:
        print("file not found")

    #main game loop
    running = True
    while running:
        screen.blit(bg,(0,0)) #black backgrund

        #handle events, this will contain more in future
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        player.update()

        platform_group.draw(screen)
        player.draw()

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main_menu()

#quit/exit
pygame.quit()
sys.exit()

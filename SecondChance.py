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

# Load background music
pygame.mixer.music.load('assets/music/TestSong.mp3')

# Set initial volume
volume = 0.5  # Initial volume level (between 0 and 1)
pygame.mixer.music.set_volume(volume)

pygame.mixer.music.play(-1)  # Start playing background music on a loop

#color
RED = (255, 0, 0)

def main_menu():
    # Create menu
    menu = pygame_menu.Menu('Second Chance', screen_width, screen_height, theme=pygame_menu.themes.THEME_BLUE)

    # Add buttons to the menu
    menu.add.button('Start Game', game_loop)
    menu.add.button("Instructions", instructions_menu)
    menu.add.button("Leaderboard", leaderboard_menu)
    menu.add.button("Options", options_menu)
    menu.add.button('Quit', pygame_menu.events.EXIT)

    # Run menu
    menu.mainloop(screen)

def instructions_menu():
    instructions_menu = pygame_menu.Menu('Instructions', screen_width, screen_height, theme=pygame_menu.themes.THEME_BLUE)

    # Add game instructions
    instructions_text = "To move, use left and right arrow keys, or a and d\nTo jump, use up arrow key, or spacebar"
    instructions_menu.add.label(instructions_text, max_char=-1, font_size=20)

    # Add back button
    instructions_menu.add.button('Back', main_menu)

    instructions_menu.mainloop(screen)

def leaderboard_menu():
    leaderboard_menu = pygame_menu.Menu('Leaderboard', screen_width, screen_height, theme=pygame_menu.themes.THEME_BLUE)

    # Add game instructions
    instructions_text = "Work in progress"
    leaderboard_menu.add.label(instructions_text, max_char=-1, font_size=20)

    # Add back button
    leaderboard_menu.add.button('Back', main_menu)

    leaderboard_menu.mainloop(screen)

def options_menu():
    # Create options menu
    options_menu = pygame_menu.Menu('Options', screen_width, screen_height, theme=pygame_menu.themes.THEME_BLUE)

    # Add volume control buttons
    volume_label = options_menu.add.label('Volume: {}'.format(int(volume * 100)))
    volume_label.update_font({'size': 30})  # Set font size for the label

    options_menu.add.button('Increase Volume', increase_volume)
    options_menu.add.button('Decrease Volume', decrease_volume)

    # Add back button
    options_menu.add.button('Back', main_menu)

    # Run options menu
    options_menu.mainloop(screen)

def increase_volume():
    global volume
    volume = min(volume + 0.1, 1.0)  # Increase volume by 0.1, but ensure it doesn't exceed 1.0
    pygame.mixer.music.set_volume(volume)

def decrease_volume():
    global volume
    volume = max(volume - 0.1, 0.0)  # Decrease volume by 0.1, but ensure it doesn't go below 0.0
    pygame.mixer.music.set_volume(volume)

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

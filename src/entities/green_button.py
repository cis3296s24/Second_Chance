import sys

import pygame


class GreenButton:
    def __init__(self, screen, color, x, y, width, height):
        self.screen = screen
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def display(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.x <= mouse_pos[0] <= self.x + self.width and \
                            self.y <= mouse_pos[1] <= self.y + self.height:
                        running = False

            # Clear the screen
            self.screen.fill((255, 255, 255))

            # Draw the button
            pygame.draw.rect(self.screen, self.color, (self.x, self.y, self.width, self.height))

            # Update the display
            pygame.display.flip()

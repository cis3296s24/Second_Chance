import pygame

import src.entities.sprite as sp


class SpriteSheet:

    def __init__(self, filename):
        """Load the sheet."""
        try:
            self.sheet = pygame.image.load(filename).convert()
        except pygame.error as e:
            print(f"Unable to load spritesheet image: {filename}")
            raise SystemExit(e)

    def get_sprite_list(self, rows, cols, width, height, scale, skip=None, pos=None) -> list[sp.Sprite]:
        """Returns a list of sprites.

        :param rows: Number of rows in spritesheet
        :param cols: Number of columns in spritesheet
        :param width: Width of each sprite
        :param height: Height of each sprite
        :param scale: Scale multiplier of each sprite
        :param skip: A tuple of numbers to skip
        :param pos: A list of tuples for where to set each sprite's rect
        """

        # Extract individual sprites
        sprites = []
        pos_index = 0
        for y in range(rows):
            for x in range(cols):
                if (y, x) in skip: continue  # Skip chosen sprites

                # Calculate the position of the sprite in the spritesheet
                sprite_x = x * width
                sprite_y = y * height

                # Create a subsurface representing the current sprite
                surface = self.sheet.subsurface((sprite_x, sprite_y, width, height))
                surface = pygame.transform.scale(surface, (width * scale, height * scale))
                if pos is None:
                    rect = surface.get_rect()
                else:
                    rect = surface.get_rect(topleft=(pos[pos_index]))
                    pos_index += 1
                    if pos_index == len(pos): pos_index = 0

                sprite = sp.Sprite(surface, rect)

                # Append the sprite to the list of sprites
                sprites.append(sprite)

        return sprites

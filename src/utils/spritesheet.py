import pygame
import src.entities.sprite as sp

class SpriteSheet:
    """A class to load in a spritesheet.

    Attributes:
        sheet (pygame.Surface): Surface object of the loaded spritesheet.
    """

    def __init__(self, filename):
        """
        Loads the spritesheet.
        
        Args:
            filename (str): Path of the spritesheet to load.
        
        Raises:
            SystemExit: If spritesheet could not be loaded.
        """
        try:
            self.sheet = pygame.image.load(filename).convert()
        except pygame.error as e:
            print(f"Unable to load spritesheet image: {filename}")
            raise SystemExit(e)

    def get_sprite_list(self, rows, cols, width, height, scale, skip=None, pos=None) -> list[sp.Sprite]:
        """Returns a list of sprites.

        Note:
            This method assumes that all sprites in the spritesheet have the
            same widths and heights.

        Args:
            rows (int): Number of rows in spritesheet.
            cols (int): Number of columns in spritesheet.
            width (int): Width of each sprite.
            height (int): Height of each sprite.
            scale (int): Scale multiplier of each sprite.
            skip (tuple, optional): A tuple of numbers to skip. Defaults to None.
            pos (tuple, optional): A list of tuples for where to set each sprite's rect. Defaults to None.

        Returns:
            list[sp.Sprite]: The list of sprites.
        """
        # Extract individual sprites
        sprites = []
        pos_index = 0
        for y in range(rows):
            for x in range(cols):
                if (y, x) in skip: continue # Skip chosen sprites
                
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

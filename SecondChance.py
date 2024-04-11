import pygame as pg
import sys

from src.constants import *
from src.states.state_manager import StateManager
from src.states.state import State

class Game:
    """The Game class contains the main game loop.
    """
    
    def __init__(self):
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pg.time.Clock()
        self.running = True
        self.username = "" 

        
        pg.display.set_caption("Second Chance")
        
        self.load_assets()
        
        # Associate all States created afterward with this game object instance
        # and the game's state manager
        setattr(State, "game", self)
        self.manager = StateManager()
        setattr(State, "manager", self.manager)

    def run(self):
        self.get_username() # get username before running game

        while self.running:
            events = pg.event.get()
            for event in events:
                if event.type == pg.QUIT:
                    self.running = False
                if event.type == pg.K_ESCAPE:
                    self.running = False

            self.manager.state.handle_events(events)
            self.manager.state.update(events)
            self.manager.state.draw()
            pg.display.update()
            self.clock.tick(FRAME_RATE)
            
    def load_assets(self):
        self.assets_dir = os.path.join("assets")
        self.character_dir = os.path.join(self.assets_dir, "characters")
        self.background_dir = os.path.join(self.assets_dir, "backgrounds")
        self.resources_dir = os.path.join("resources")

    def get_username(self):
        # This method prompts the user for a username before starting the game
        input_rect = pg.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 12, 200, 24)
        font = pg.font.Font(None, 24)
        active = False
        
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    if input_rect.collidepoint(event.pos):
                        active = not active
                    else:
                        active = False
                if event.type == pg.KEYDOWN:
                    if active:
                        if event.key == pg.K_RETURN:
                            return
                        elif event.key == pg.K_BACKSPACE:
                            self.username = self.username[:-1]
                        else:
                            self.username += event.unicode

            self.screen.fill((30, 30, 30))
            pg.draw.rect(self.screen, (255, 255, 255), input_rect, 2)
            text_prompt = font.render("Enter your username: ", True, (255, 255, 255))
            text_prompt_rect = text_prompt.get_rect(midbottom=input_rect.topleft)
            self.screen.blit(text_prompt, text_prompt_rect)
            # Render the username directly inside the input rectangle
            text_surface = font.render(self.username, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=input_rect.center)
            self.screen.blit(text_surface, text_rect)
            pg.display.flip()

            
if __name__ == "__main__":
    pg.init()
    g = Game()
    g.run()
    pg.quit()
    sys.exit()
    
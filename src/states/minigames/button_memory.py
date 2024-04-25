import collections
import pygame as pg
import os
import random


import src.utils.spritesheet as spritesheet
from src.states.state import State
from src.states.minigames.minigame import Minigame
from src.utils.timer import Timer

pg.mixer.init()


class ButtonMemory(Minigame):
    """A minigame to test your memory."""

    def __init__(self):
        instructions = (
            "The goal of this minigame is to follow the pattern displayed "
            "on the screen and copy it afterwards by using the arrow keys."
        )

        img = "button_memory.jpg"

        super().__init__(instructions, img=os.path.join("minigames", img))

        # Minigame specific attributes
        self.categories = ["normal", "green", "red"]
        self.category = "normal"
        self.arrow_types = ["up", "left", "down", "right"]

        # Top left position to display arrows as a unit
        self.unit_pos = collections.namedtuple("Point", ["x", "y"])(315, 375)
        self.arrow_pos = (  # Defining arrow positions manually yes
            (self.unit_pos.x + 64, self.unit_pos.y),  # UP
            (self.unit_pos.x, self.unit_pos.y + 64),  # LEFT
            (self.unit_pos.x + 64, self.unit_pos.y + 64),  # DOWN
            (self.unit_pos.x + 128, self.unit_pos.y + 64),  # RIGHT
        )
        self.key = None
        self.key_to_index = {
            "up": 0,
            "left": 1,
            "down": 2,
            "right": 3,
        }
        self.arrows = self.get_arrow_dict()
        self.colored_arrow = None

        self.start_time = 0
        self.display_time = 0.32  # Number of seconds a key press should be displayed
        self.delay_timer = Timer(start=True)
        self.has_pressed = False
        self.countdown_over = False
        self.should_display_buttons = True

        self.sequence_current_index = -1
        self.sequence_length = 5
        self.random_sequence = self.generate_random_sequence(self.sequence_length)

        self.user_sequence = []
        self.sequence_text = "Your presses: "
        self.sequence_text_surf = pg.Surface((0, 0))
        self.win_text = ""
        self.lose_text = ""

    def handle_events(self, events):
        super().handle_events(events)  # To enable pause menu access

        for event in events:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    self.key = "up"
                elif event.key == pg.K_LEFT:
                    self.key = "left"
                elif event.key == pg.K_DOWN:
                    self.key = "down"
                elif event.key == pg.K_RIGHT:
                    self.key = "right"
                if self.key:
                    self.has_pressed = True
                    self.sequence_current_index += 1
                    play_key_sound()

    def update(self, events):
        super().update(events)

        if self.countdown_over and self.should_display_buttons:
            # Override the minigame timer because it was started after countdown
            self.timer = Timer() 
            self.should_display_buttons = False
            self.manager.set_state(
                ButtonDisplayer(
                    self.random_sequence,
                    self.arrows,
                    self.display_time,
                    self.timer,
                ),
                save_prev=True,
            )
            return

        index = self.key_to_index.get(self.key, -1)

        # If enough time has passed, change arrow back to normal
        current_time = self.delay_timer.get_time(ms=True)
        if current_time - self.start_time > self.display_time:
            self.category = "normal"

        if self.has_pressed:
            self.has_pressed = False
            self.start_time = current_time

            # If key correct
            if self.key == self.random_sequence[self.sequence_current_index]:
                self.user_sequence.append(self.key)
                self.sequence_text += self.key.capitalize() + " "
                self.category = "green"
            else:  # Key incorrect
                self.category = "red"
                self.won = False

            # Win condition
            if self.user_sequence == self.random_sequence:
                self.won = True
                return

        self.colored_arrow = self.arrows[self.category][index]
        self.sequence_text_surf = self.get_text_surface(self.sequence_text, "green", 36)

    def draw(self):
        super().draw()  # Draw minigame background

        # Draw normal arrows
        for arrow in self.arrows["normal"]:
            self.screen.blit(arrow.surface, arrow.rect)

        if self.colored_arrow:
            self.screen.blit(self.colored_arrow.surface, self.colored_arrow.rect)

        self.screen.blit(self.sequence_text_surf, (20, 20))

    def get_arrow_spritesheet(self, image):
        """Return a spritesheet of the arrow image in the folder it's currently
        located in.

        Args:
            image (str): Image file name.

        Returns:
            Spritesheet object of the loaded arrow image. 
        """
        return spritesheet.SpriteSheet(
            os.path.join(self.game.assets_dir, "images", image)
        )

    def get_arrow_dict(self):
        """
        Returns a dictionary containing the arrow type names as keys, and
        a list of arrow `Sprite` objects for each key.

        Returns:
            dict[str, list[Sprite]]: Dictionary of arrow names to list of 
                sprites.
        """
        arrows = {}

        arrow_width = arrow_height = 32

        arrow_sheet = self.get_arrow_spritesheet("arrow_keys.png")
        arrow_sheet_green = self.get_arrow_spritesheet("arrow_keys_blue.png")
        arrow_sheet_red = self.get_arrow_spritesheet("arrow_keys_red.png")
        scale = 2
        skip = ((0, 0), (0, 2))  # Row-col of images to skip
        rows = 2
        cols = 3

        for category in self.categories:
            arrows[category] = []
            if category == "normal":
                sheet = arrow_sheet
            elif category == "green":
                sheet = arrow_sheet_green
            elif category == "red":
                sheet = arrow_sheet_red

            sprite_list = sheet.get_sprite_list(
                rows, cols, arrow_width, arrow_height, scale, skip, self.arrow_pos
            )

            for i, arrow_type in enumerate(self.arrow_types):
                arrows[category].append(sprite_list[i])

        return arrows

    def generate_random_sequence(self, length):
        """
        Return a sequence of randomly generated arrow keys of a certain
        length (with replacement).

        Args:
            length (int): Length of sequence.

        Returns:
            list[str]: A random sequence of arrows.
        """
        return random.choices(self.arrow_types, k=length)


class ButtonDisplayer(State):
    """This state shows the correct sequence of buttons to the player.

    Args:
        sequence (list[str]): A random sequence of arrows.
        arrows (dict[str, list[Sprite]]): Dictionary of arrow names to list of 
            sprites.
        time_delay (float): Amount of time that between each arrow press.
        minigame_timer (Timer): Timer from minigame.
    """

    def __init__(self, sequence, arrows, time_delay, minigame_timer):
        
        super().__init__()
        self.sequence = sequence
        self.arrows = arrows
        self.colored_arrow = None
        self.key_to_index = {
            "up": 0,
            "left": 1,
            "down": 2,
            "right": 3,
        }

        self.time_delay = time_delay
        self.minigame_timer = minigame_timer
        self.timer = Timer(start=True)
        self.start_time = 0
        self.category = "normal"

        self.current_sequence_index = -1  # Start at -1
        self.text = self.get_text_surface("Watch closely", "green", 42)

    def update(self, events):
        current_time = self.timer.get_time(ms=True)

        if current_time < 2:
            self.category = "normal"
        # If certain amount of time has passed, reset time and toggle
        elif current_time - self.start_time > self.time_delay:
            self.start_time = current_time

            # Toggle the arrow color
            self.category = "green" if self.category == "normal" else "normal"
            if self.category == "green":
                self.current_sequence_index += 1
                if self.current_sequence_index < len(self.sequence):
                    play_key_sound()

        if 0 <= self.current_sequence_index <= len(self.sequence) - 1:
            current_arrow = self.sequence[self.current_sequence_index]
            index = self.key_to_index.get(current_arrow, -1)
            self.colored_arrow = self.arrows[self.category][index]

        if self.current_sequence_index == len(self.sequence):
            self.manager.pop_state()
            self.minigame_timer.start()

    def draw(self):
        # Draw normal arrows
        for arrow in self.arrows["normal"]:
            self.screen.blit(arrow.surface, arrow.rect)

        if self.colored_arrow:
            self.screen.blit(self.colored_arrow.surface, self.colored_arrow.rect)

        self.screen.blit(self.text, (310, 300))


key_press_sound = pg.mixer.Sound("assets/soundeffects/key_press.wav")


def play_key_sound():
    """Plays a sound when an arrow key is pressed."""
    key_press_sound.play()

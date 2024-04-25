import pygame as pg

from ..state import State


class WinScreen(State):
    def __init__(self):
        super().__init__("background.png")

    def handle_events(self, events: list[pg.event.Event]):
        from .title_screen import TitleScreen
        for event in events:
            if event.type != pg.KEYDOWN:
                return
            if event.key == pg.K_RETURN:
                self.manager.set_state(TitleScreen)

    def draw(self):
        super().draw()
        self.screen.blit(
            pg.font.Font(None, 36).render("You win!", True, "black"),
            (self.screen.get_width() / 2, self.screen.get_height() - 100)
        )

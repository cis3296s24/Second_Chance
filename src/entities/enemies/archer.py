from .enemy import Enemy
from src.entities.attack import RangeAttack
import pygame as pg

attacks = pg.sprite.Group()
class archer(Enemy):
    def __init__(self, x, y, platform_group, scroll):
        super().__init__(
            x, y,
            platform_group,
            scroll,
            "archer",
            2,
            0,
            0.5,
            100,
            100,
            30
        )
        self.health_bar_offset_x = (self.rect.width - self.health_bar_length) / 2
        self.health_bar_offset_y = self.rect.height / 2 - 30
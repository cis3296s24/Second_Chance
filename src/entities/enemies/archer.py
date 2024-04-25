import pygame as pg

from src.entities.attack import RangeAttack
from .enemy import Enemy

attacks = pg.sprite.Group()


class archer(Enemy):
    def __init__(self, x, y, platform_group, tile_list):
        super().__init__(
            x, y,
            platform_group,
            tile_list,
            "archer",
            speed=2,
            vertical_speed=0,
            gravity=0.5,
            health=100,
            max_health=100,
            strength=20
        )
        range_attack = RangeAttack(self.rect.centerx + 10, self.rect.centery, self.direction, damage_value=10)
        attacks.add(range_attack)
        attacks.update()
        attacks.draw(self.screen)
        self.health_bar_offset_x = (self.rect.width - self.health_bar_length) / 2
        self.health_bar_offset_y = self.rect.height / 2 - 30

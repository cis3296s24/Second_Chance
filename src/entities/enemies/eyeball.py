from .enemy import Enemy

class Eyeball(Enemy):
    def __init__(self, x, y, min_x, max_x, platform_group):
        super().__init__(
            x, y, min_x, max_x,
            platform_group,
            "eyeball",
            speed=2,
            vertical_speed=0,
            gravity=0.5,
            health=100,
            max_health=100,
            strength=20
        )
        self.health_bar_offset_x = (self.rect.width - self.health_bar_length) / 2
        self.health_bar_offset_y = self.rect.height / 2 - 30 
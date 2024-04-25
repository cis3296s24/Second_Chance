from src.objects.portal import Portal  # Import portal class
from .level import Level


class Level1_1(Level):
    def __init__(self):
        imgArr = [f"plx-{i}.png" for i in range(1, 6)]
        super().__init__(
            level=1,
            music_file="levelmusic.mp3",
            imgArr=imgArr
        )

    def create_platforms(self):
        # for i in range(1, 6):
        #     self.platforms.add(Platform(i * 100, i * 100))
        # self.objects.add(self.platforms)
        pass

    def spawn_enemies(self):
        # self.enemies.add(Eyeball(300, 600, self.platforms))
        # self.enemies.add(Skeleton(500, 600, self.platforms))
        # self.enemies.add(archer(100, 200, self.platforms))
        # self.enemies.add(Wolf(700, 600, self.platforms))
        pass

    def add_portal(self):
        # Add portal at specific coordinates
        self.portal = Portal(3500, 400, "assets/backgrounds/portal.png", 150, 150)
        self.portals.add(self.portal)
        self.objects.add(self.portals)

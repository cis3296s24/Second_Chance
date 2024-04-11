from .level import Level
from src.objects.platforms import Platform
from src.entities.enemies.eyeball import Eyeball  # Import the Eyeball class
from src.entities.enemies.skeleton import Skeleton  # Import the Skeleton class
from src.objects.portal import Portal # Import portal class

class Level1_1(Level):
    def __init__(self):
        imgArr = [f"plx-{i}.png" for i in range(1, 6)]
        super().__init__(
            level=1,
            music_file="levelmusic.mp3",
            imgArr=imgArr
        )
        
    def create_platforms(self):
        for i in range(1, 6):
            self.platforms.add(Platform(i * 100, i * 100))

    def spawn_enemies(self):
        self.enemies.add(Eyeball(300, 600, self.platforms, self.scroll))
        self.enemies.add(Skeleton(500, 600, self.platforms, self.scroll))

    def add_portal(self):
        # Add portal at specific coordinates
        self.portal = Portal(3500, 500, 50, 50)
        self.portals.add(self.portal)
        
        


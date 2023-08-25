import csv
import pygame

# Max
class Map():
    def __init__(self, filename: str) -> None:
        self.map = []
        self.tiles = [None for _ in range(38)]
        with open(f"game/map/{filename}") as f:
            f = csv.reader(f, delimiter=",")
            for row in f:
                self.map.append(row)

        self.size = 50

    def draw(self, screen: pygame.surface) -> None:
        """ Draws tiles on screen

        Args:
            screen: surface to blit onto
        """
        for x in range(len(self.map)):
            for y in range(len(self.map[x])):
                if self.tiles[int(self.map[x][y])] == None:
                    self.tiles[int(self.map[x][y])] = pygame.image.load(f"game/sprites/tiles/{self.map[x][y]}.png").convert() # disable alpha, speeds up game
                screen.blit(pygame.transform.scale(self.tiles[int(self.map[x][y])], (self.size, self.size)), (y * self.size, x * self.size, self.size, 5))
    
    def get_tile_map(self) -> list[pygame.Rect]:
        """ Loops through tiles list and creates a list for collidable and uncollidable tiles

        Returns:
            Two lists, a list of collidables and list of uncollidables
        """

        # collidables < 23 and > 33
        tiles = []
        collidables = []
        for x in range(len(self.map)):
            for y in range(len(self.map[x])):
                if int(self.map[x][y]) < 23 or int(self.map[x][y]) > 33:
                    collidables.append(pygame.Rect(y * self.size, x * self.size, self.size, self.size))
                else:
                    tiles.append(pygame.Rect(y * self.size, x * self.size, self.size, self.size))

        return collidables, tiles

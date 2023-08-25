import random
import pygame

from game.entity.gums.auto_gum import Auto_weapon
from game.entity.gums.shotgum import Shotgun
from game.entity.gums.sniper import Sniper
from game.entity.player.character import Character

class Item():
    items = []
    def __init__(self, x: int, y: int, image: str) -> None:
        self.rect = pygame.Rect(x, y, 25, 25)
        self.image = pygame.image.load(image)
        Item.items.append(self)

    def update(self, character: Character) -> None:
        """ checks for collision between player and item

        Args: 
           character: character object, the player you are currently playing

        """
        if character.boxCollider.colliderect(self.rect):
            self.use(character)
            Item.items.remove(self)

    def draw(self, screen: pygame.surface) -> None:
        """ Draws item onto screen

        Args: 
           screen: surface to blit onto

        """
        screen.blit(pygame.transform.scale(self.image, [40, 40]), self.rect)

    def use(self, character: Character) -> None:
        """ Uses item

        Args: 
           character: character object, the player you are currently playing

        """
        pass

class Ammo(Item):
    def __init__(self, x: int, y: int, image: str) -> None:
        super().__init__(x, y, image)

    def use(self, character: Character) -> None:
        """ Fully replenishes ammo for current weapon

        Args: 
           character: character object, the player you are currently playing

        """
        if character.current_slot != 0:
            character.guns[character.current_slot].t_ammo = character.guns[character.current_slot].max_ammo

class ExtraHealth(Item):
    def __init__(self, x: int, y: int, image: str) -> None:
        super().__init__(x, y, image)

    def use(self, character: Character) -> None:
        """ Adds one heart to total player hearts

        Args: 
           character: character object, the player you are currently playing

        """
        if character.get_hearts() < character.max_hearts:
            character.set_hearts(1)

class ExtraShield(Item):
    def __init__(self, x: int, y: int, image: str) -> None:
        super().__init__(x, y, image)

    def use(self, character: Character) -> None:
        """ Adds one shield to total player shields

        Args: 
           character: character object, the player you are currently playing

        """
        if character.get_shields() < character.max_shield:
            character.set_shields(1)

class Chest(Item):
    def __init__(self, x: int, y: int, image: str) -> None:
        super().__init__(x, y, image)
        self.weapons = [Auto_weapon(x, y), Shotgun(x, y), Sniper(x, y)]

    def use(self, character: Character) -> None:
        """ Appends random weapon to player inventory

        Args: 
           character: character object, the player you are currently playing

        """
        i = random.randrange(0, 3)
        character.guns.append(self.weapons[i])
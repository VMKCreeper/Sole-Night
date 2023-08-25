import pygame
import math
from game.entity.animation import Animation
from game.sprites.image_load import enemy_attack

class Bullet:
    _bullet_index = 0
    bullets = []

    def __init__(self, x: int, y: int, angle: float, speed: float, bullet_type: int, tag: str, damage: int):

        self.index = Bullet.get_index()
        Bullet.add_index(1)
        self.tag = tag
        self.bullets = enemy_attack(str(bullet_type))
        self.animation = Animation(3)

        self.rect = pygame.Rect(x, y, 10, 10)
        self.damage = damage

        self.dx = math.cos(angle) * speed
        self.dy = math.sin(angle) * speed
        self.angle = angle

        # accuracy fix
        self.x = self.rect.x
        self.y = self.rect.y

    def update(self, tiles, player, enemies):
        self.x += self.dx
        self.y += self.dy

        self.rect.x = self.x
        self.rect.y = self.y

        if self.rect.collidelist(tiles) >= 0:
            Bullet.bullets[self.index] = None

        if self.rect.colliderect(player.boxCollider) and player.i_frames == 0 and self.tag == "enemy":
            if player.get_shields() > 0:
                # go through shield
                if self.damage > player.get_shields():
                    player.set_hearts(-(self.damage - player.get_shields()))
                    player._shields = 0
                else:
                    player.set_shields(-self.damage)
            else:
                player.set_hearts(-self.damage)
            player.i_frames = 120
            Bullet.bullets[self.index] = None

        for enemy in enemies:
            if self.rect.colliderect(enemy.rect) and self.tag == "player":
                enemy.hp -= self.damage
                Bullet.bullets[self.index] = None

    def draw(self, SCREEN):
        self.animation.animate(self.bullets)

        SCREEN.blit(pygame.transform.rotate(self.bullets[self.animation.frame_num], 360 - math.degrees(self.angle)),
                    [self.rect.x - 20, self.rect.y - 20])

    @classmethod
    def get_index(cls) -> int:
        return cls._bullet_index

    @classmethod
    def set_index(cls, num: int) -> None:
        cls._bullet_index = num

    @classmethod
    def add_index(cls, num: int) -> None:
        cls._bullet_index += num

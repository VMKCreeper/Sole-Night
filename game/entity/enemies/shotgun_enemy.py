from game.entity.enemies.enemy import Enemy
from game.entity.bullet import Bullet

import math


class ShotgunEnemy(Enemy):
    def __init__(self, x: int, y: int, character):
        # Movement
        self.move_delay_clamp = [60, 180]
        self.move_toward_multiplier = 0.7
        self.move_away_multiplier = 0.3

        # Fire
        self.fire_delay_clamp = [180, 300]
        self.fire_subtick = 15
        self.fire_times = 2

        # Self
        super().__init__(x, y, character)
        self._name = "Shotgun"
        self.hp = 30
        self.max_hp = 30
        self.speed = 3
        self.color = [255, 150, 80]

        self.damage = 1

    def fire(self, direction: float):
        Bullet.bullets.append(
            Bullet(self.rect.x, self.rect.y, direction - math.radians(40), 3, 1, Enemy.tag, self.damage))
        Bullet.bullets.append(
            Bullet(self.rect.x, self.rect.y, direction - math.radians(20), 3, 1, Enemy.tag, self.damage))
        Bullet.bullets.append(
            Bullet(self.rect.x, self.rect.y, direction, 3, 1, Enemy.tag, self.damage))
        Bullet.bullets.append(
            Bullet(self.rect.x, self.rect.y, direction + math.radians(20), 3, 1, Enemy.tag, self.damage))
        Bullet.bullets.append(
            Bullet(self.rect.x, self.rect.y, direction + math.radians(40), 3, 1, Enemy.tag, self.damage))

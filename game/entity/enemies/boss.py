import math
import random
import pygame
from typing import List

from game.entity.bullet import Bullet


class Boss:
    def __init__(self, x: int, y: int, character):
        self._name = "Boss"
        self.frozen = False
        self.hp = 1000
        self.max_hp = 1000
        self.rect = pygame.Rect(x, y, 100, 100)
        self.color = [100, 0, 130]
        self.speed = 5

        self.character = character
        self.tick = 0

        self.current_pattern = "Idle"
        self.charge_dir = 0

        self.damage = 1


    def update(self, platforms: List):
        self.frozen = False
        self.tick += 1
        # Idle state
        if self.current_pattern == "Idle":
            self.move_toward(self.speed, self.get_direction(), platforms)
            if self.tick >= 60:
                self.tick = 0
                self.current_pattern = random.choice(["Spray", "Charge"])

        # Spray Bullets to Player
        elif self.current_pattern == "Spray":
            if self.tick % 6 == 0:
                Bullet.bullets.append(Bullet(self.rect.centerx, self.rect.centery, self.get_direction(
                ) + random.uniform(-0.25, 0.25), 10, 1, "enemy", self.damage))

            if self.tick >= 300:
                self.tick = 0
                self.current_pattern = "Idle"
                self.speed = random.randint(-2, 2) * 2

        # Charge toward Player after short time
        elif self.current_pattern == "Charge":
            if self.tick <= 120:
                self.color = [130, 0, 110]
                self.charge_dir = self.get_direction()
            else:
                self.move_toward(50, self.charge_dir, platforms)

            if self.tick >= 150:
                self.color = [100, 0, 130]
                self.tick = 0
                self.current_pattern = "Idle"

    def get_direction(self) -> float:
        x_diff = self.character.boxCollider.centerx - self.rect.centerx
        y_diff = self.character.boxCollider.centery - self.rect.centery

        direction = math.atan2(y_diff, x_diff)

        if direction < 0:
            direction += math.radians(360)

        return direction

    def move_toward(self, speed: float, direction: float, platforms: List) -> None:
        dx = math.cos(direction) * speed
        dy = math.sin(direction) * speed

        self.rect.x = self.rect.x + dx
        for tile in platforms:
            if self.rect.colliderect(tile):
                if dx < 0:
                    self.rect.left = tile.right
                elif dx > 0:
                    self.rect.right = tile.left

        self.rect.y = self.rect.y + dy
        for tile in platforms:
            if self.rect.colliderect(tile):
                if dy < 0:
                    self.rect.top = tile.bottom
                elif dy > 0:
                    self.rect.bottom = tile.top

    def draw(self, SCREEN: pygame.Surface):
        pygame.draw.rect(SCREEN, self.color, self.rect)

        # hp
        pygame.draw.rect(SCREEN, (0, 0, 0),
                         [self.rect.x, self.rect.y - 25, 100, 20])
        pygame.draw.rect(SCREEN, (255, 0, 0),
                         [self.rect.x, self.rect.y - 25, self.hp * 100 / self.max_hp, 20])
        pygame.draw.rect(SCREEN, (0, 0, 0),
                         [self.rect.x, self.rect.y - 25, 100, 20], 4)

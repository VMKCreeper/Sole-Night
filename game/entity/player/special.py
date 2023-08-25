import random

import pygame
from game.entity.animation import Animation
import math

def selected_special(sprite):
    if sprite == "Canadian" or sprite == "Vegapunk":
        return DamageArea, 87
    elif sprite == "Super Cop":
        return Stealth, 0
    elif sprite == "Insane Cat":
        # explosion on top of cat, damages everyone nearby
        return Explosion, 65

class Special:
    def __init__(self, cd, frames, frame_rate, on):
        self.cd_time = cd
        self.time_waited = 0
        self.used = 0
        self.frames = frames
        self.animation = Animation(frame_rate)
        self.bar_rect = pygame.Rect([25, 125, 300, 30])
        self.on = on

    def draw(self, screen, x, y):
        # draw + animate
        if self.frames is not None and self.used == -1:
            screen.blit(self.frames[self.animation.frame_num], [x, y])
            self.animation.animate(self.frames)

    def cd_bar(self, surface):
        if not self.used:
            self.bar_rect.width = 150
        else:
            self.bar_rect.width = self.time_waited / self.cd_time * 150

        s = pygame.Surface((abs(self.bar_rect.width), 30))
        s.set_alpha(175)
        s.fill((0, 44, 115))
        surface.blit(s, (20, 170))
        pygame.draw.rect(surface, (0, 0, 0), [20, 170, 150, 30], 5)

    def cooldown(self):
        if self.time_waited >= self.cd_time:
            self.time_waited = 0
            self.used = 0
        elif self.used == 1:
            # self.time_waited = 0 as soon as you press the button
            self.time_waited += 1

    def enemy_dist(self, boxCollider, enemy):
        x_diff = boxCollider[0] - enemy.rect.x + 5
        y_diff = boxCollider[1] - enemy.rect.y + 25
        distance = math.sqrt((x_diff * x_diff) + (y_diff * y_diff))

        return distance

    def active_count(self, time):
        if self.used == -1:
            self.on -= 1

        if not self.on:
            self.used = 1
            self.animation.frame_num = 0
            self.on = time

class DamageArea(Special):
    def __init__(self, cd, frames):
        super().__init__(cd, frames, 5, 480)
        self.loc = (0, 0)

    def sort_enemies(self, boxCollider, enemies):
        targets = self.collect_enemies(boxCollider, enemies)

        for i in range(len(targets)):
            min_loc = i
            for n in range(i + 1, len(targets)):
                if targets[n] < targets[min_loc]:
                    min_loc = n
            targets[i], targets[min_loc] = targets[min_loc], targets[i]

        self.loc = (targets[0][1] - 50, targets[0][2] - 55)

    def collect_enemies(self, boxCollider, enemies):
        targets = []
        for enemy in enemies:
            distance = self.enemy_dist(boxCollider, enemy)
            targets.append((distance, enemy.rect.x - 20, enemy.rect.y - 20))

        return targets

    def passive_damage(self, enemies):
        for enemy in enemies:
            x_diff = self.loc[0] - enemy.rect.x + 90
            y_diff = self.loc[1] - enemy.rect.y + 90
            distance = math.sqrt((x_diff * x_diff) + (y_diff * y_diff))

            if self.used == -1 and distance <= 90:
                if random.randrange(1, 100) == 1 and not enemy.frozen:
                    enemy.frozen = True
            elif self.used == 1:
                enemy.frozen = False

class Explosion(Special):
    def __init__(self, cd, frames):
        super().__init__(cd, frames, 2, None)

    def explode_damage(self, boxCollider, enemies):
        if self.animation.frame_num >= len(self.frames) - 1:
            self.used = 1
            self.animation.frame_num = 0

        for enemy in enemies:
            distance = self.enemy_dist(boxCollider, enemy)

            if self.used == -1 and distance <= 125:
                enemy.hp -= 30

class Stealth(Special):
    def __init__(self, cd):
        super().__init__(cd, None, None, 300)

    def player_opacity(self, frame):
        opacity = 100 if (1 - (self.on / 300)) * 255 < 100 else (1 - (self.on / 300)) * 255
        # the player is more transparent and slowly fades back to normal with the cool down
        frame.set_alpha(opacity)
import pygame
import math
from game.entity.bullet import Bullet
from game.entity.enemies.enemy import Enemy
from game.entity.player.character import Character

class Companion:
    def __init__(self, x: int, y: int) -> None:
        self.rect = pygame.Rect(x, y, 40, 40)
        self.fire_tick = 60
        self.speed = 3

    def update(self, enemies: list[Enemy], player: Character, platforms: list[pygame.Rect]) -> None:
        """ Performs updates on companion (movement, distance caluculations...)

        Args:
            enemies: list of enemies
            player: Character object, the character you are playing as
            platforms: list of collidable tiles
        
        """
        # movement
        diff_x = player.boxCollider.x - self.rect.x
        diff_y = player.boxCollider.y - self.rect.y

        distance = math.sqrt(math.pow(diff_x, 2) + math.pow(diff_y, 2))
        angle = math.atan2(diff_y, diff_x)
        
        dx = math.cos(angle)
        dy = math.sin(angle)

        if abs(distance) > 100:
            self.move(dx, dy, platforms)
        elif abs(distance) < 90:
            self.move(-dx, -dy, platforms)
        
        enemy_queue = []
        distance_queue = []

        for enemy in enemies:
            diff_x = enemy.rect.x - self.rect.x
            diff_y = enemy.rect.y - self.rect.y

            distance = math.sqrt(math.pow(diff_x, 2) + math.pow(diff_y, 2))
            
            enemy_queue.append(enemy)
            distance_queue.append(round(distance))

        if len(enemy_queue) > 0:
            self.sort_enemies(distance_queue, enemy_queue)

        # fire
            if self.fire_tick > 0:
                self.fire_tick -= 1
            else:
                diff_x = enemy_queue[0].rect.x - self.rect.x + 10
                diff_y = enemy_queue[0].rect.y - self.rect.y + 10

                angle = math.atan2(diff_y, diff_x)

                Bullet.bullets.append(Bullet(self.rect.x, self.rect.y, angle, 20, 5, "player", 5))
                self.fire_tick = 60

    def draw(self, surface: pygame.surface) -> None:
        """ Draws companion onto screen

        Args:
            surface: surface to blit onto

        """
        pygame.draw.rect(surface, (255, 255, 255), self.rect)

    def move(self, dx: int, dy: int, platforms: list[pygame.Rect]) -> None:
        """ Moves companion and checks for collision

        Args:
            dx: distance in x axis
            dy: distance in y axis
            platforms: list of collidable tiles

        """
        self.rect.x += dx * self.speed
        for tile in platforms:
            if self.rect.colliderect(tile):
                if dx < 0:
                    self.rect.left = tile.right
                elif dx > 0:
                    self.rect.right = tile.left
                    
        self.rect.y += dy * self.speed
        for tile in platforms:
            if self.rect.colliderect(tile):
                if dy < 0:
                    self.rect.top = tile.bottom
                elif dy > 0:
                    self.rect.bottom = tile.top
    
    def sort_enemies(self, distance_list, enemy_list):
        for i in range(len(distance_list) - 1):
            for j in range(i + 1, len(distance_list)):
                if distance_list[i] > distance_list[j]:
                    if enemy_list[i].damage > enemy_list[j].damage and distance_list[i]//100 == distance_list[j]//100:
                        continue
                    distance_list[i], distance_list[j] = distance_list[j], distance_list[i]
                    enemy_list[i], enemy_list[j] = enemy_list[j], enemy_list[i]

                
from game.entity.enemies.enemy import Enemy
from game.entity.bullet import Bullet


class SniperEnemy(Enemy):
    def __init__(self, x: int, y: int, character):
        # Movement
        self.move_delay_clamp = [180, 360]
        self.move_toward_multiplier = 3
        self.move_away_multiplier = 1

        # Fire
        self.fire_delay_clamp = [300, 420]
        self.fire_subtick = 5
        self.fire_times = 1

        # Self
        super().__init__(x, y, character)
        self._name = "Sniper"
        self.hp = 25
        self.max_hp = 25
        self.speed = 2
        self.color = [0, 90, 10]

        self.damage = 4

    def fire(self, direction: int):
        Bullet.bullets.append(
            Bullet(self.rect.x, self.rect.y, direction, 25, 4, Enemy.tag, self.damage))

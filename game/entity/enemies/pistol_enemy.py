from game.entity.enemies.enemy import Enemy
from game.entity.bullet import Bullet


class PistolEnemy(Enemy):
    def __init__(self, x: int, y: int, character):
        # Movement
        self.move_delay_clamp = [60, 180]
        self.move_toward_multiplier = 1
        self.move_away_multiplier = 0.5

        # Fire
        self.fire_delay_clamp = [120, 240]
        self.fire_subtick = 20
        self.fire_times = 3

        # Self
        super().__init__(x, y, character)
        self._name = "Pistol"
        self.hp = 15
        self.max_hp = 15
        self.speed = 3
        self.color = [200, 100, 100]

        self.damage = 2

    def fire(self, direction: float) -> None:
        Bullet.bullets.append(
            Bullet(self.rect.x, self.rect.y, direction, 5, 2, Enemy.tag, self.damage))

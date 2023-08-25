import math
from game.entity.bullet import Bullet
from game.entity.gums.default_stat import Default


class Shotgun(Default):
    def __init__(self, x, y) -> None:
        super().__init__(x, y)
        self.ammo = 5
        self.t_ammo = 30
        self.max_ammo = 30
        self.cooldown = 60
        self.name = "Shotgum"

        self.damage = 8

    def fire(self):
        if self.ammo > 0:
            Bullet.bullets.append(Bullet(self.rect.x, self.rect.y, self.get_direction() - math.radians(20), 7, 3, Default.tag, self.damage)) 
            Bullet.bullets.append(Bullet(self.rect.x, self.rect.y, self.get_direction() - math.radians(10), 7, 3, Default.tag, self.damage))
            Bullet.bullets.append(Bullet(self.rect.x, self.rect.y, self.get_direction(), 7, 3, Default.tag, self.damage))
            Bullet.bullets.append(Bullet(self.rect.x, self.rect.y, self.get_direction() + math.radians(10), 7, 3, Default.tag, self.damage))
            Bullet.bullets.append(Bullet(self.rect.x, self.rect.y, self.get_direction() + math.radians(20), 7, 3, Default.tag, self.damage))
            self.ammo -= 1

    def reload(self):
        if self.t_ammo > 5:
            self.t_ammo -= 5 - self.ammo
            self.ammo = 5
        else:
            self.ammo = self.t_ammo
            self.t_ammo = 0
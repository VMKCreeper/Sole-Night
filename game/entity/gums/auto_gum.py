from game.entity.bullet import Bullet
from game.entity.gums.default_stat import Default

class Auto_weapon(Default):
    def __init__(self, x, y) -> None:
        super().__init__(x, y)
        self.ammo = 30
        self.t_ammo = 300
        self.max_ammo = 300
        self.cooldown = 10
        self.name = "Auto Gum"

        self.damage = 6

    def fire(self):
        if self.ammo > 0:
            Bullet.bullets.append(Bullet(self.rect.x, self.rect.y, self.get_direction(), 10, 3, Default.tag, self.damage))
            self.ammo -= 1

    def reload(self):
        if self.t_ammo > 30:
            self.t_ammo -= 30 - self.ammo
            self.ammo = 30
        else:
            self.ammo = self.t_ammo
            self.t_ammo = 0
    
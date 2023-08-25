from game.entity.bullet import Bullet
from game.entity.gums.default_stat import Default


class Smgum(Default):
	def __init__(self, name, ammo, t_ammo, cooldown, x, y) -> None:
		super().__init__(x, y, t_ammo)
		self.name = name
		self.ammo = 15
		# self.t_ammo = 450
		self.cooldown = 0.5

	def fire(self):
		Bullet.bullets.append(Bullet(10, 10, self.get_direction(), 8, 4))

	def reload(self):
		self.t_ammo = (self.ammo + self.t_ammo)
		self.t_ammo - 15
		self.ammo = 15

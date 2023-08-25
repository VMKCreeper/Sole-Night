from game.entity.bullet import Bullet
from game.entity.gums.default_stat import Default

class Akimbo(Default):
	def __init__(self, name, ammo, t_ammo, cooldown, x, y) -> None:
		super().__init__(x, y, t_ammo)
		self.name = name
		self.ammo = 16
		# self.t_ammo = 480
		self.cooldown = 0.6

	def fire(self):
		Bullet.bullets.append(Bullet(10, 10, self.get_direction(), 15, 7))

	def reload(self):
		self.t_ammo = (self.ammo + self.t_ammo)
		self.t_ammo - 16
		self.ammo = 16

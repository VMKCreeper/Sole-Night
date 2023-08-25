from game.entity.bullet import Bullet
from game.entity.gums.default_stat import Default

class Backup(Default):
	def __init__(self, x, y) -> None:
		super().__init__(x, y)
		self.cooldown = 30
		self.name = "Hand gum"

		self.damage = 4

	def fire(self):
		Bullet.bullets.append(Bullet(self.rect.x, self.rect.y, self.get_direction(), 10, 3, Default.tag, self.damage))

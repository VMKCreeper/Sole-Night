import pygame
import math

class Default:
	tag = "player"
	def __init__(self, x, y) -> None:
		self.rect = pygame.Rect(x, y, 10, 10)
		self.ammo = "∞"
		self.t_ammo = "∞"

	def update(self, x, y):
		self.rect.x = x + 20
		self.rect.y = y + 40

	def draw(self, SCREEN):
		# pygame.draw.rect(SCREEN, (255, 255, 255), self.rect)
		pass

	def get_direction(self) -> float:
		mouse_x, mouse_y = pygame.mouse.get_pos()
		
		distance_x = mouse_x - self.rect.centerx
		distance_y = mouse_y - self.rect.centery
		
		angle = math.atan2(distance_y, distance_x)

		return angle
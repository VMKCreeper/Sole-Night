import pygame
import math
import random
from typing import List

class Enemy:

	tag = "enemy"
	def __init__(self, x, y, character):
		self.character = character
		self.rect = pygame.Rect(x, y, 30, 30)
		
		self.distance = 0
		self.direction = 0
		self.scatter_offset = 0
		
		self.move_tick = 0
		self.move_delay = 0		#random.randint(self.move_delay_clamp[0], self.move_delay_clamp[1])
		self.movement = "Idle"
		
		self.fire_tick = 0
		self.fire_count = 0
		self.fire_delay = random.randint(self.fire_delay_clamp[0], self.fire_delay_clamp[1])

		self.frozen = False
	
	def update(self, platforms):
		# Maths
		x_diff = self.character.boxCollider.x - self.rect.x + 30  # offset
		y_diff = self.character.boxCollider.y - self.rect.y + 40 # offset
		distance = math.sqrt((x_diff * x_diff) + (y_diff * y_diff))
		if self.movement == "Move Toward":
			self.direction = self.get_direction(x_diff, y_diff)
		
		# Movement
		## Assign Movement
		self.move_tick += 1
		if self.move_tick >= self.move_delay:
			self.move_tick = 0
			self.move_delay = random.randint(self.move_delay_clamp[0], self.move_delay_clamp[1])
			
			if distance >= self.character.detection_radius * self.move_toward_multiplier:
				self.movement = "Move Toward"
			else:
				self.movement = "Move Away"
				self.scatter_offset = random.uniform(-math.pi/4, math.pi/4)
		
		if distance <= self.character.detection_radius * self.move_away_multiplier:
			self.move_tick = 0
			self.movement = "Move Away"
			self.scatter_offset = 0

		## Move
		if self.movement == "Move Away":
			self.move(-math.cos(self.direction + self.scatter_offset), -math.sin(self.direction + self.scatter_offset), platforms)
		
		elif self.movement == "Move Toward":
			self.move(math.cos(self.direction), math.sin(self.direction), platforms)

		# Fire
		self.fire_tick += 1
		if self.fire_tick >= self.fire_delay:
			if not (type(self.character.special_attk).__name__ == "Stealth" and self.character.special_attk.used == -1):
				sub_tick = self.fire_tick - self.fire_delay
				if sub_tick % self.fire_subtick == 0:
					self.fire_count += 1
					self.fire(self.get_direction(x_diff, y_diff))
					if self.fire_count >= self.fire_times:
						self.fire_tick = 0
						self.fire_count = 0
						self.fire_delay = random.randint(self.fire_delay_clamp[0], self.fire_delay_clamp[1])
	
	
	def move(self, dx, dy, platforms):
		self.rect.x = self.rect.x + dx * self.speed
		for tile in platforms:
			if self.rect.colliderect(tile):
				if dx < 0:
					self.rect.left = tile.right
				elif dx > 0:
					self.rect.right = tile.left
					
		self.rect.y = self.rect.y + dy * self.speed
		for tile in platforms:
			if self.rect.colliderect(tile):
				if dy < 0:
					self.rect.top = tile.bottom
				elif dy > 0:
					self.rect.bottom = tile.top


	def draw(self, SCREEN):
		pygame.draw.rect(SCREEN, self.color, self.rect)

		# hp
		pygame.draw.rect(SCREEN, (0, 0, 0), [self.rect.x, self.rect.y - 15, 30, 5])
		pygame.draw.rect(SCREEN, (255, 0, 0), [self.rect.x, self.rect.y - 15, self.hp * 30 / self.max_hp, 5])
		pygame.draw.rect(SCREEN, (0, 0, 0), [self.rect.x, self.rect.y - 15, 30, 5], 1)

	def get_direction(self, x_diff: int, y_diff: int) -> float:
		"""
		x_diff: integer
		y_diff: integer

		calculate the angle in radian
		convert angle to positive (0 ~ 2 pi)
		"""
		direction = math.atan2(y_diff, x_diff)

		if direction < 0:
			direction += math.radians(360)

		return direction

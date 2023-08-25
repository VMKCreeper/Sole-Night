import pygame
from pygame import *

from game.entity.animation import Animation
from game.entity.enemies.enemy import Enemy
from game.entity.gums.backup_weapon import Backup

import game.sprites.image_load as image_load
from game.entity.player.special import selected_special, Explosion

class Character():
	def __init__(self, x: int, y: int, name: str, is_continuing: bool = False) -> None:
		self.boxCollider = pygame.Rect(x, y, 40, 85)
		self.velocity = pygame.Vector2()
		self.speed = 4
		self.detection_radius = 350
		self.dodging = -1
		self.dodge_speed = 0
		self.dodge_cooldown = 360
		self.i_frames = 0
		self.reloading = -1
		
		# slots
		self.guns = [Backup(x, y)]
		self.gun_cooldown = 0
		self.current_slot = 0

		# animation
		self.animation = Animation(9)
		self.data = image_load.player_data(name)
		self.player = image_load.player_data(name)
		self.idle_frames = image_load.load(self.player["file_name"], 6, "i")
		self.run_frames = image_load.load(self.player["file_name"], 5, "r")
		self.flipped = False
		self.special_frames = image_load.specials(selected_special(self.data["sprite"])[1], self.data["special"])

		# stats
		from game.gamemanager import GameManager
		self._hearts = self.player["hearts"] if not is_continuing else GameManager.progress["HP"]
		GameManager.progress["HP"] = self._hearts
		self._shields = self.player["shield"]
		self.special_cd = self.player["cd"]

		self.max_hearts = self.player["hearts"]
		self.max_shield = self.player["shield"]
		self.regen_speed = self.player["regen_speed"]
		if self.data["sprite"] != "Super Cop":
			self.special_attk = selected_special(self.data["sprite"])[0](self.special_cd, self.special_frames)
		else:
			self.special_attk = selected_special(self.data["sprite"])[0](self.special_cd)

		self.counter = 0

		self.mouse = (0, 0)

	def update(self, platforms: list[pygame.Rect]) -> None:
		""" Performs update on player (dodge, movement, shoot, reload...)
		Args:
			platform: list of collidable objects

		"""
		self.dodge()
		self.move(platforms)

		if self.i_frames > 0:
			self.i_frames -= 1

		if self._shields != self.max_shield:
			self.shield_regen()

		# gun
		self.guns[self.current_slot].update(self.boxCollider.x, self.boxCollider.y)
		if self.gun_cooldown > 0:
			self.gun_cooldown -= 1

		if self.reloading > 0:
			self.reloading -= 1
		elif self.reloading == 0:
			self.guns[self.current_slot].reload()
			self.reloading = -1
		
		if self.special_attk.used == 1:
			self.special_attk.cooldown()

	def move(self, platforms: list[pygame.Rect]) -> None:
		""" Moves character and checks for collision

		Args:
			platform: list of collidable objects

		"""
		self.boxCollider.x += self.velocity.x
		#check x collision
		for tile in platforms:
			if self.boxCollider.colliderect(tile):
				if self.velocity.x < 0:
					self.boxCollider.left = tile.right
				elif self.velocity.x > 0:
					self.boxCollider.right = tile.left

		self.boxCollider.y += self.velocity.y
		#check y collision
		for tile in platforms:
			if self.boxCollider.colliderect(tile):
				if self.velocity.y < 0:
					self.boxCollider.top = tile.bottom
				elif self.velocity.y > 0:
					self.boxCollider.bottom = tile.top

	def draw(self, screen: pygame.surface) -> None:
		""" Draws character onto screen

		Args:
			screen: surface to blit onto

		"""
		# pygame.draw.rect(screen, (0, 0, 255), self.boxCollider)
		frame = self.run_frames[self.animation.frame_num] if self.velocity else self.idle_frames[self.animation.frame_num]
	
		if self.data["special"] == "stealth" and self.special_attk.used == -1:
			self.special_attk.player_opacity(frame)
		elif self.i_frames > 0:
			self.animation.flicker(frame)
		else:
			frame.set_alpha(255)
		
		screen.blit(frame, [self.boxCollider.x - 10, self.boxCollider.y - 2])

		if self.i_frames > 0:
			self.animation.flicker(frame)
		# else:
		#     frame.set_alpha(255)
		screen.blit(frame, [self.boxCollider.x - 10, self.boxCollider.y - 2])

		# gun
		self.guns[self.current_slot].draw(screen)

		if self.special_attk.used == -1 and self.data["special"] == "kamziazie":
			self.special_attk.draw(screen, self.boxCollider.x - 235, self.boxCollider.y - 215)
		elif self.special_attk.frames is not None and self.data["special"] == "freezing":
			self.special_attk.draw(screen, self.special_attk.loc[0], self.special_attk.loc[1])

	def flip_frames(self) -> None:
		""" Flips the character sprite when facing another direction 

		"""
		self.run_frames = self.animation.flip(self.run_frames)
		self.idle_frames = self.animation.flip(self.idle_frames)
		self.flipped = not self.flipped

	def keyInputs(self, events: pygame.event, keys: list[pygame.event.Event], enemies_list: list[Enemy]) -> None:  
		""" Checks for key presses and responds accordingly

		Args:
			events: list of pygame events
			keys: list of keys

		"""
		if pygame.key.get_pressed()[keys[0]]: # w
			self.velocity.y = -self.speed
		elif pygame.key.get_pressed()[keys[2]]: # s
			self.velocity.y = self.speed

		if pygame.key.get_pressed()[keys[3]]: # d
			self.velocity.x = self.speed
			if not self.flipped:
				self.flip_frames()
		elif pygame.key.get_pressed()[keys[1]]: # a
			self.velocity.x = -self.speed
			if self.flipped:
				self.flip_frames()
		if pygame.key.get_pressed()[keys[9]] and not self.special_attk.used: # special attack
			self.special_attk.used = -1

			if self.data["sprite"] == "Canadian":
				self.special_attk.sort_enemies(self.boxCollider, enemies_list)

			if self.data["sprite"] == "Insane Cat":
				self.set_hearts(-2)

		# hold to fire
		if pygame.mouse.get_pressed()[0]:
			if self.gun_cooldown == 0 and self.reloading == -1:
				self.guns[self.current_slot].fire()
				self.gun_cooldown = self.guns[self.current_slot].cooldown
			
		for event in events:
			if event.type == KEYDOWN:
				if event.key == keys[4]: # dodge
					if self.dodging < 0 and self.dodge_cooldown >= 120: 
						self.dodging = 20
						self.dodge_cooldown -= 120
					else:
						self.dodging = -1
				if event.key == keys[5] and self.current_slot != 0: # reload
					self.reloading = 60

				for i in range(len(self.guns)):
					if event.key == keys[i + 6] and self.guns[i]:
						self.gun_cooldown = 0
						self.reloading = -1
						self.current_slot = i

			if event.type == KEYUP:
				if event.key == keys[1] and self.velocity.x < 0 or event.key == keys[3] and self.velocity.x > 0:
					self.velocity.x = 0
				
				if event.key == keys[0] and self.velocity.y < 0 or event.key == keys[2] and self.velocity.y > 0:
					self.velocity.y = 0

			if event.type == pygame.MOUSEBUTTONDOWN:
				self.mouse = pygame.mouse.get_pos()
		
	def dodge(self) -> None:
		""" Player dodges

		"""
		if self.dodge_cooldown < 360:
			self.dodge_cooldown += 1

		if self.dodging >= 0:
			self.i_frames = 20
			if self.dodging <= 5:
				self.dodge_speed -= 2
			elif self.dodging >= 15:
				self.dodge_speed += 2

			if self.velocity.x > 0:
				self.velocity.x = self.dodge_speed
			elif self.velocity.x < 0:
				self.velocity.x = -self.dodge_speed

			if self.velocity.y < 0:
				self.velocity.y = -self.dodge_speed
			elif self.velocity.y > 0:
				self.velocity.y = self.dodge_speed
			
			self.dodging -= 1
		else:
			self.dodge_speed = 0
			
	def shield_regen(self) -> None:
		""" Regenerates player shield over time

		"""
		self.counter += 1
		if self.counter == self.regen_speed:
			self.counter = 0
			self._shields = min(self._shields + 1, self.max_shield)

	def get_hearts(self) -> int:
		""" Fetches player hearts

		Returns: 
			return players current hearts

		"""
		return self._hearts

	def set_hearts(self, hearts: int) -> None:
		""" Changes player hearts

		Args: 
		hearts: amount of hearts to add / subract to total 

		"""
		self._hearts += hearts

	def get_shields(self) -> int:
		""" Fetches player shields

		Returns: 
			returns player current shields

		"""
		return self._shields

	def set_shields(self, shield: int) -> None:
		""" Changes player shields

		Args: 
		shield: amount of shield to add / subract to total 

		"""
		self._shields += shield
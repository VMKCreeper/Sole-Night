from typing import List
import json
import pygame
from game.view.title_view import TitleView

from game.view.my_game import MyGame
from game.view.base_view import BaseView
from game.sprites.image_load import lose_screen, win_screen, mainmenu_button

class EndScreen(BaseView):
	def __init__(self, done, coins) -> None:
		pygame.mouse.set_visible(True)
		self.done = done
		self.coins = coins
		self.mainmenu_button = pygame.Rect(375, 625, 200, 50)
		self.font = pygame.font.SysFont('Tahoma', 50)

		# Kill Count
		from game.gamemanager import GameManager
		self.kill_count_list = self.sort_kill_counts(GameManager.progress)

		# Reset Stored Data
		with open("game/data/progress.json", "w") as f:
			reset = {"Character": "ERROR: NO CHARACTER", "Level": 0, "Pistol": 0, "Shotgun": 0, "Sniper": 0, "Boss": 0}
			json.dump(reset, f, indent=4)

	def event_loop(self, events: List[pygame.event.Event]) -> None:
		for event in events:
			if event.type == pygame.locals.MOUSEBUTTONDOWN:
				if self.mainmenu_button.collidepoint(event.pos):
					MyGame.set_current_view(TitleView())

	def update(self) -> None:
		pass

	def draw(self, surface: pygame.Surface) -> None:
		if self.done:
			surface.blit(win_screen, [0, 0])
		else:
			surface.blit(lose_screen, [0, 0])

		surface.blit(mainmenu_button, self.mainmenu_button)

		coins = self.font.render(f"Coins: {self.coins}", True, (255, 255, 255))
		text_rect = coins.get_rect(center = (700, 100))
		surface.blit(coins, text_rect)

		# Display Kill Count
		for i in range(len(self.kill_count_list)):
			item = self.kill_count_list[i]
			stat_text = self.font.render(f"{item[1]}: {item[0]}", True, (255, 255, 255))
			
			surface.blit(stat_text, (50, 700 - 80*i))

	# Show Statistics
	def sort_kill_counts(self, progress) -> List:
		kill_count_list = []
		kill_count_list.append([progress["Pistol"], "Pistol"])
		kill_count_list.append([progress["Shotgun"], "Shotgun"])
		kill_count_list.append([progress["Sniper"], "Sniper"])
		kill_count_list.append([progress["Boss"], "Boss"])

		return self.merge_sort(kill_count_list)

	def merge_sort(self, list: List) -> List:
		# print(list)
		if len(list) <= 1:
			return list
		
		divider = len(list)//2
		first_list = self.merge_sort(list[:divider])
		second_list = self.merge_sort(list[divider:])

		# Merge
		sorted_list = []
		while len(first_list) > 0 and len(second_list) > 0:
			if first_list[0] < second_list[0]:
				sorted_list.append(second_list.pop(0))
			else:
				sorted_list.append(first_list.pop(0))
		
		if len(first_list) > 0:
			sorted_list += first_list
		elif len(second_list) > 0:
			sorted_list += second_list

		return sorted_list

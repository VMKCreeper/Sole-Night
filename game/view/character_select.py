import json
from typing import List

import pygame
from game.sprites.image_load import *

from game.view.my_game import MyGame
from game.view.base_view import BaseView

class CharacterSelect(BaseView):
    def __init__(self) -> None:
        self.buttons = [pygame.Rect(625, 585, 188, 73), pygame.Rect(25, 25, 128, 61)]
        self.currentCharacter = 0
        self.characters = ["Insane Cat", "Super Cop", "Canadian"]
        self.icons = [cat_icon, cop_icon, can_icon]
        self.images = []

        with open("game/data/store.json", "r") as f:
            self.store = json.load(f)

        self.game_text = pygame.font.SysFont('Times New Roman', 20)
        self.coins_text = pygame.font.SysFont('Times New Roman', 45)
        
        for i in range(3):
            source = player_data(self.characters[i])
            self.images.append(pygame.image.load(f"game/sprites/{source['file_name']}/{source['file_name']}_i1.png"))
            self.buttons.append(pygame.Rect(150 + i * 400, 175, 300, 350))

    def event_loop(self, events: List[pygame.event.Event]) -> None:
        for event in events:
            if event.type == pygame.locals.MOUSEBUTTONDOWN:
                for i in range(len(self.buttons)):
                    if self.buttons[i].collidepoint(event.pos):
                        if i == 0:
                            from game.view.play_view import PlayView
                            MyGame.set_current_view(PlayView(self.characters[self.currentCharacter]))
                        elif i == 1:
                            from game.view.title_view import TitleView
                            MyGame.set_current_view(TitleView())
                        elif i == 2:
                            self.currentCharacter = 0
                        elif i == 3:
                            if self.store['unlocked'][1]:
                                self.currentCharacter = 1
                            elif self.store['coins'] >= 500:
                                self.store['coins'] -= 500
                                self.store['unlocked'][1] = True
                                with open("game/data/store.json", "w") as f:
                                    json.dump(self.store, f, indent=4)
                        elif i == 4:
                            if self.store['unlocked'][2]:
                                self.currentCharacter = 2
                            elif self.store['coins'] >= 1000:
                                self.store['coins'] -= 1000
                                self.store['unlocked'][2] = True
                                with open("game/data/store.json", "w") as f:
                                    json.dump(self.store, f, indent=4)

    def update(self) -> None:
        pass

    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(blurred_title, [0, 0])
        for button in self.buttons:
            if self.buttons.index(button) != 1 and self.buttons.index(button) != 0:
                pygame.draw.rect(surface, (255, 255, 255), button)
        surface.blit(back_button, [25, 25])
        surface.blit(play_button, [625, 585])

        pygame.draw.rect(surface, (175, 175, 175), self.buttons[self.currentCharacter + 2], 5)

        # characters
        for i in range(3):
            surface.blit(self.icons[i], (self.buttons[i+2].x, self.buttons[i+2].y))
            if not self.store['unlocked'][i]:
                unlock_text = self.game_text.render(f"Unlock: ${500 * i}", True, (255, 255, 255))
                surface.blit(unlock_text, (self.buttons[i+2].x + 95, self.buttons[i+2].y + 365))

        # currency
        currency_text = self.coins_text.render(f"Coins: ${self.store['coins']}", True, (255, 255, 255))
        surface.blit(currency_text, (1120, 58))

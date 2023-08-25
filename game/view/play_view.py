from typing import List

import pygame
from pygame import *

from game.view.my_game import MyGame
from game.view.base_view import BaseView
from game.view.pause_view import PauseView

from game.gamemanager import GameManager
from game.sprites.image_load import cursor, hit_cursor


class PlayView(BaseView):
    def __init__(self, character, is_continuing=False) -> None:
        self.game_manager = GameManager(character, is_continuing)
        self.cursor_img = cursor
        pygame.mouse.set_visible(False)

    def event_loop(self, events: List[pygame.event.Event]) -> None:
        self.game_manager.player.keyInputs(events, self.game_manager.keys, self.game_manager.level.enemies_list)
        for event in events:
            if event.type == pygame.locals.KEYDOWN:
                if event.key == pygame.locals.K_p:
                    MyGame.set_current_view(PauseView(self))

    def update(self) -> None:
        self.game_manager.update()

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill((255, 255, 255))
        surface.set_alpha(None)  # optimaization
        self.game_manager.draw(surface)

        # cursor
        cursor_loc = (pygame.mouse.get_pos()[
                      0] + 11, pygame.mouse.get_pos()[1] + 12)
        draw_loc = (pygame.mouse.get_pos()[
                    0] - 12, pygame.mouse.get_pos()[1] - 12)
        self.cursor_img = cursor
        for enemy in self.game_manager.level.enemies_list:
            if enemy.rect.collidepoint(cursor_loc):
                self.cursor_img = hit_cursor
                break

        surface.blit(self.cursor_img, draw_loc)

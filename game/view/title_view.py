import pygame
import json

from game.view.base_view import BaseView
from game.view.my_game import MyGame
from game.view.settings_view import SettingsView
from game.view.character_select import CharacterSelect

from game.entity.animation import Animation
import game.sprites.image_load as image_load


class TitleView(BaseView):
    frames = image_load.title_frames()

    def __init__(self):
        pygame.mouse.set_visible(True)
        self.buttons = [pygame.Rect(607, 455, 187, 73), pygame.Rect(
            607, 555, 187, 73), pygame.Rect(1290, 703, 56, 55)]
        self.animation = Animation(6)

        self.info_font = pygame.font.SysFont("Arial", 25)
        self.continue_text = self.info_font.render(
            "Continue", True, (255, 255, 255))

    def event_loop(self, events):
        for event in events:
            if event.type == pygame.locals.MOUSEBUTTONDOWN:
                for i in range(len(self.buttons)):
                    if self.buttons[i].collidepoint(event.pos):
                        if i == 0:
                            MyGame.set_current_view(CharacterSelect())
                        elif i == 1:
                            temp = {}
                            with open("game/data/progress.json", "r") as f:
                                temp = json.load(f)
                            if temp["Level"] == 0:
                                print(
                                    "Whats the point of continuing in First Level?")
                            else:
                                from game.view.play_view import PlayView
                                MyGame.set_current_view(
                                    PlayView(temp["Character"], True))
                        elif i == 2:
                            MyGame.set_current_view(SettingsView())

    def update(self):
        self.animation.animate(self.frames)

    def draw(self, surface: pygame.Surface):
        surface.blit(self.frames[self.animation.frame_num], [0, 0])

        surf_center = surface.get_rect().center
        text_rect = image_load.title_text.get_rect()
        text_rect.center = surf_center
        text_rect.y = surface.get_height() * 0.35
        surface.blit(image_load.title_text, text_rect.topleft)

        # play button
        text_rect = image_load.play_button.get_rect()
        text_rect.center = surf_center
        text_rect.y = surface.get_height() * 0.57
        surface.blit(image_load.play_button, text_rect.topleft)

        surface.blit(image_load.settings_button, [1290, 703])

        # Continue Button
        text_rect = image_load.continue_button.get_rect()
        text_rect.center = surf_center
        text_rect.y = surface.get_height() * 0.69
        surface.blit(image_load.continue_button, text_rect.topleft)

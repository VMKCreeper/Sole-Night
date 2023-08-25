import json
from typing import List
from game.view.my_game import MyGame
from game.view.base_view import BaseView
from game.sprites.image_load import *


class SettingsView(BaseView):
    def __init__(self) -> None:
        self.buttons = pygame.Rect(25, 25, 128, 61)
        self.volume_bar_rect = pygame.Rect(469, 180, 800, 25)
        self.instructions = [instructions1, instructions2,
                             instructions3, instructions4, instructions5, instructions6]
        self.slider_loc = 600

    def event_loop(self, events: List[pygame.event.Event]) -> None:
        for event in events:
            if event.type == pygame.locals.MOUSEBUTTONDOWN:
                if self.buttons.collidepoint(event.pos):
                    from game.view.title_view import TitleView
                    MyGame.set_current_view(TitleView())

        if pygame.mouse.get_pressed()[0] and self.volume_bar_rect.collidepoint(pygame.mouse.get_pos()):
            volume = (pygame.mouse.get_pos()[
                      0] - 469) / self.volume_bar_rect.width
            self.slider_loc = pygame.mouse.get_pos()[0]
            pygame.mixer.music.set_volume(volume)

    def update(self) -> None:
        pass

    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(blurred_title, (0, 0))
        surface.blit(back_button, [25, 25])

        surface.blit(volume_text, [116, 150])
        surface.blit(volume_bar, [469, 180])
        pygame.draw.circle(surface, (0, 0, 0), [self.slider_loc, 190], 27)

        for i in range(6):
            surface.blit(self.instructions[i], [180, 295 + 70 * i])

        surface.blit(credits_text, [630, 290])

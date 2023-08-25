from typing import List

import pygame

from game.view.my_game import MyGame
from game.view.base_view import BaseView


class TemplateView(BaseView):
    def __init__(self) -> None:
        pass

    def event_loop(self, events: List[pygame.event.Event]) -> None:
        for event in events:
            pass

    def update(self) -> None:
        pass

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill((255, 255, 255))
        pygame.draw.circle(surface, (0, 0, 200), (50, 50), 30)

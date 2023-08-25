from abc import ABC, abstractmethod

import pygame
import pygame.locals

from game.view.base_view import BaseView


class BaseGame(ABC):
    game: 'BaseGame' = None

    def __init__(self) -> None:
        BaseGame.game = self
        pygame.init()
        pygame.font.init()

        pygame.mixer.init()
        pygame.mixer.music.load('game/soundtrack.mp3')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.1)

        WIDTH = 1400
        HEIGHT = 800
        SIZE = (WIDTH, HEIGHT)

        self.screen = pygame.display.set_mode(SIZE)
        self.clock = pygame.time.Clock()
        self.current_view: BaseView = None

        self.create()

    @staticmethod
    def set_current_view(view: BaseView) -> None:
        BaseGame.game.current_view = view

    @abstractmethod
    def create(self) -> None: ...

    def run(self):
        running = True
        while running:
            # EVENT HANDLING
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.locals.KEYDOWN:
                    if event.key == pygame.locals.K_ESCAPE:
                        running = False
                elif event.type == pygame.locals.QUIT:
                    running = False

            self.current_view.event_loop(events)
            self.current_view.update()
            self.current_view.draw(self.screen)

            # Must be the last two lines
            # of the game loop
            pygame.display.flip()
            self.clock.tick(60)
            # ---------------------------

        pygame.quit()

import pygame

from game.view.base_view import BaseView
from game.view.my_game import MyGame


class PauseView(BaseView):
    def __init__(self, parent: BaseView):
        self.parent = parent
        title_font = pygame.font.SysFont("Arial", 40)
        self.title_text = title_font.render("Paused", True, (255, 255, 255))

        info_font = pygame.font.SysFont("Arial", 25)
        self.info_text1 = info_font.render(
            "Press 'p' to return", True, (175, 175, 175))
        self.info_text2 = info_font.render(
            "Press 'q' to quit", True, (175, 175, 175))

    def event_loop(self, events):
        for event in events:
            if event.type == pygame.locals.KEYDOWN:
                if event.key == pygame.locals.K_p:
                    MyGame.set_current_view(self.parent)
                if event.key == pygame.locals.K_q:
                    from game.view.title_view import TitleView
                    title_view = TitleView()
                    MyGame.set_current_view(title_view)

    def update(self):
        pass

    def draw(self, surface: pygame.Surface):
        # draw parent screen
        self.parent.draw(surface)

        # Draw overlay
        overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        surface.blit(overlay, (0, 0))

        surf_center = surface.get_rect().center
        text_rect = self.title_text.get_rect()
        text_rect.center = surf_center
        text_rect.y = surface.get_height() * 0.33
        surface.blit(self.title_text, text_rect.topleft)

        # Un-pause info
        text_rect = self.info_text1.get_rect()
        text_rect.center = surf_center
        text_rect.y = surface.get_height() * 0.67
        surface.blit(self.info_text1, text_rect.topleft)

        # quit info
        text_rect = self.info_text2.get_rect()
        text_rect.center = surf_center
        text_rect.y = surface.get_height() * 0.67 + text_rect.height + 10
        surface.blit(self.info_text2, text_rect.topleft)

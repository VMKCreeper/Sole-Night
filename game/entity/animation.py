import pygame
import pygame.transform

class Animation:
    opacity = 255

    def __init__(self, frame_rate) -> None:
        self.frame_num = 0
        self.frame_rate = frame_rate
        self.fps = 0
        self.fade_out = True

    def animate(self, frame_list) -> None:
        self.fps += 1

        if self.fps >= self.frame_rate:
            self.frame_num += 1
            self.fps = 0

        if self.frame_num >= len(frame_list):
            self.frame_num = 0

    def flicker(self, image) -> None:
        if self.fade_out:
            self.opacity -= 10
        elif not self.fade_out:
            self.opacity += 10

        if self.opacity >= 255:
            self.fade_out = True
        elif self.opacity <= 50:
            self.fade_out = False

        image.set_alpha(self.opacity)

    @staticmethod
    def filled_area(colour) -> pygame.Surface:
        area = pygame.Surface((1400, 800), 0)
        area.fill(colour)

        return area

    @staticmethod
    def masking(enemy, surface):
        enemy_rect = pygame.Surface([enemy.rect.width, enemy.rect.height])
        enemy_rect.blit(Animation.filled_area((135, 206, 235)), [0, 0], [0, 0, 1400, 800])
        surface.blit(enemy_rect, (enemy.rect.x, enemy.rect.y), surface.get_rect().clip([0, 0, 1400, 800]))

    @staticmethod
    def flip(frame_list) -> list[pygame.Surface]:
        flipped_frames = []
        for frame in frame_list:
            flipped_frames.append(pygame.transform.flip(frame, True, False))

        return flipped_frames

    @classmethod
    def fade_out_screen(cls, area, speed):
        if cls.opacity > 0:
            cls.opacity -= speed

            area.set_alpha(cls.opacity)
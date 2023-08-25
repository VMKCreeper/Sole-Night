import json
import pygame

def player_data(name):
    with open("game/data/entity_stats.json", "r") as f:
        data = json.load(f)

    for player in data:
        if player["sprite"] == name:
            return player

# can be further improved by making it all one function...
def load(location, maximum, action):
    frames = []
    for image in range(1, maximum):
        frame = pygame.image.load(f"game/sprites/{location}/{location}_{action}{image}.png").convert_alpha()
        frames.append(frame)

    return frames

def enemy_attack(location):
    frames = []
    for image in range(1, 16):
        attk = pygame.image.load(f"game/sprites/bullets/{location}/{image}.png").convert_alpha()
        attk = pygame.transform.scale2x(attk)
        frames.append(attk)

    return frames

def loading_screen():
    frames = []
    all_black = pygame.Surface([1400, 800])
    all_black.fill((0, 0, 0))
    frames.append(all_black)

    for image in range(1, 5):
        loading = pygame.image.load(f"game/sprites/menu_images/loading_{image}.png").convert()
        frames.append(loading)
    return frames

def title_frames():
    frames = []
    for image in range(1, 99):
        frame = pygame.image.load(f"game/sprites/title_imgs/title_bg ({image}).png").convert()
        frame = pygame.transform.smoothscale(frame, [1401, 853])
        frames.append(frame)

    return frames

def specials(max, location):
    frames = []
    for image in range(1, max):
        frame = pygame.image.load(f"game/sprites/{location}/{location} ({image}).png").convert_alpha()
        if location == "freezing":
            frame = pygame.transform.scale(frame, [200, 200])
        frames.append(frame)

    return frames

pygame.init()
pygame.display.set_mode((1400, 800))

hit_cursor = pygame.image.load("game/sprites/hit_cursor.png").convert_alpha()
hit_cursor = pygame.transform.scale(hit_cursor, [25, 25])

cursor = pygame.image.load("game/sprites/cursor.png").convert_alpha()
cursor = pygame.transform.scale(cursor, [25, 25])

portal = pygame.image.load("game/sprites/portal.png").convert_alpha()

title_text = pygame.image.load("game/sprites/menu_images/title_text.png").convert_alpha()
settings_button = pygame.image.load("game/sprites/menu_images/settings_button.png").convert_alpha()
back_button = pygame.image.load("game/sprites/menu_images/back_button.png").convert_alpha()
play_button = pygame.image.load("game/sprites/menu_images/play_button.png").convert_alpha()
continue_button = pygame.image.load("game/sprites/menu_images/continue_button.png").convert_alpha()
mainmenu_button = pygame.image.load("game/sprites/menu_images/mainmenu_button.png").convert_alpha()

blurred_title = pygame.image.load("game/sprites/title_imgs/titlebg_blurred.png").convert()
blurred_title = pygame.transform.smoothscale(blurred_title, [1401, 853])

cop_icon = pygame.image.load("game/sprites/icons/supercop_icon.png").convert_alpha()
cat_icon = pygame.image.load("game/sprites//icons/cat_icon.png").convert_alpha()
can_icon = pygame.image.load("game/sprites//icons/can_icon.png").convert_alpha()

lose_screen = pygame.image.load("game/sprites/menu_images/lose_screen.png").convert()
win_screen = pygame.image.load("game/sprites/menu_images/win_screen.png").convert()

volume_text = pygame.image.load("game/sprites/menu_images/volume_text.png").convert_alpha()
volume_bar = pygame.image.load("game/sprites/menu_images/volume_bar.png").convert_alpha()

instructions1 = pygame.image.load("game/sprites/menu_images/in1.png").convert_alpha()
instructions1 = pygame.transform.smoothscale(instructions1, [139, 84])
instructions2 = pygame.image.load("game/sprites/menu_images/in2.png").convert_alpha()
instructions2 = pygame.transform.smoothscale(instructions2, [142, 84])
instructions3 = pygame.image.load("game/sprites/menu_images/in3.png").convert_alpha()
instructions3 = pygame.transform.smoothscale(instructions3, [196, 84])
instructions4 = pygame.image.load("game/sprites/menu_images/in4.png").convert_alpha()
instructions4 = pygame.transform.smoothscale(instructions4, [235, 84])
instructions5 = pygame.image.load("game/sprites/menu_images/in5.png").convert_alpha()
instructions5 = pygame.transform.smoothscale(instructions5, [139, 80])
instructions6 = pygame.image.load("game/sprites/menu_images/in6.png").convert_alpha()
instructions6 = pygame.transform.smoothscale(instructions6, [230, 80])
credits_text = pygame.image.load("game/sprites/menu_images/credits.png").convert_alpha()
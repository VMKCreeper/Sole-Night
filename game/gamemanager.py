import json
import random
from pygame import *

from game.map.map import Map
from game.view.endscreen_view import EndScreen
from game.view.my_game import MyGame
from game.items.item import *

from game.entity.enemies.pistol_enemy import PistolEnemy
from game.entity.enemies.shotgun_enemy import ShotgunEnemy
from game.entity.player.character import Character
from game.entity.enemies.sniper_enemy import SniperEnemy
from game.entity.enemies.boss import Boss
from game.entity.bullet import Bullet
from game.entity.companion import Companion

from game.entity.animation import Animation
from game.sprites.image_load import loading_screen
from game.sprites.image_load import portal

class GameManager():

    progress = {"Character": "ERROR: NO CHARACTER", "HP": 0,
                "Level": 0, "Pistol": 0, "Shotgun": 0, "Sniper": 0, "Boss": 0}

    keys = [K_w, K_a, K_s, K_d, K_LSHIFT, K_r, K_1, K_2, K_3, K_q]


    def __init__(self, character: Character, is_continuing: bool = False) -> None:
        if is_continuing:
            with open("game/data/progress.json") as f:
                GameManager.progress = json.load(f)
        else:
            GameManager.progress = {"Character": character, "HP": 0,
                                    "Level": 0, "Pistol": 0, "Shotgun": 0, "Sniper": 0, "Boss": 0}

        self.player = Character(
            100, 100, GameManager.progress["Character"], is_continuing)

        self.current_level = 0 if not is_continuing else GameManager.progress["Level"]

        self.level = Level(self.current_level, self.player)
        self.transition_time = 0

        self.animation = Animation(60)
        self.loading_frames = loading_screen()
        self.black_screen = Animation.filled_area((0, 0, 0))
        self.fade = False

        self.ammo_font = pygame.font.SysFont('Consolas', 50, True)
        self.gum_font = pygame.font.SysFont('Consolas', 25, True)

        self.total_coins = 0

        self.reset()

    def update(self) -> None:
        """ Monitors current state of game (changes level, save coins, switch screens)

        """
        if self.player.get_hearts() <= 0:
            self.save_coins()
            MyGame.set_current_view(EndScreen(False, self.total_coins))

        if self.transition_time > 0:
            self.transition_time -= 1
        else:
            self.level.update()

        # next level
        if self.level.done:
            self.fade = True
            self.transition_time = 300
            if self.current_level < 2:
                self.changeLevel()
            else:
                self.save_coins()
                MyGame.set_current_view(EndScreen(True, self.total_coins))

        if self.fade:
            Animation.fade_out_screen(self.black_screen, 1)
            if Animation.opacity == 0:
                self.fade = False
                Animation.opacity = 255

    def draw(self, surface: pygame.surface) -> None:
        """ Draws basic UI (health bar, shield bar, dodge bar)

        Args: 
           surface: screen to blit onto

        """
        if self.transition_time == 0:
            self.level.draw(surface)

            # health bar
            s = pygame.Surface((abs(self.player.get_hearts() * 300 / self.player.max_hearts), 30))
            s.set_alpha(175)
            s.fill((255, 0, 0))
            surface.blit(s, (20, 20))
            pygame.draw.rect(surface, (0, 0, 0), [20, 20, 300, 30], 5)

            # shield bar
            s = pygame.Surface(
                (abs(self.player.get_shields() * 300 / self.player.max_shield), 30))
            s.set_alpha(175)
            s.fill((200, 200, 200))
            surface.blit(s, (20, 70))
            pygame.draw.rect(surface, (0, 0, 0), [20, 70, 300, 30], 5)

            # dodge bar
            s = pygame.Surface((abs(150 * self.player.dodge_cooldown / 360), 30))
            s.set_alpha(175)
            s.fill((133, 251, 255))
            surface.blit(s, (20, 120))
            pygame.draw.rect(surface, (0, 0, 0), [20, 120, 150, 30], 5)
            pygame.draw.line(surface, (0, 0, 0), [70, 125], [70, 145], 5)
            pygame.draw.line(surface, (0, 0, 0), [120, 125], [120, 145], 5)

            # cd bar
            self.player.special_attk.cd_bar(surface)

            # weapons
            pygame.draw.rect(surface, (255, 255, 255), [
                             1210, 325 + self.player.current_slot * 50, 130, 50], 5)
            for i in range(len(self.player.guns)):
                gum_text = self.gum_font.render(
                    self.player.guns[i].name, True, (255, 255, 255))
                text_rect = gum_text.get_rect(center=(1275, 350 + i * 50))
                surface.blit(gum_text, text_rect)

            # ammo
            ammo_text = self.ammo_font.render(
                f"{self.player.guns[self.player.current_slot].ammo}/{self.player.guns[self.player.current_slot].t_ammo}" if self.player.reloading == -1 else 'Reloading', True, (255, 255, 255))
            text_rect = ammo_text.get_rect(center=(1200, 700))
            surface.blit(ammo_text, text_rect)
        else:
            self.animation.animate(self.loading_frames)
            surface.blit(self.loading_frames[self.animation.frame_num], [0, 0])

        if self.fade:
            surface.blit(self.black_screen, [0, 0])

    def changeLevel(self) -> None:
        """ Increase level by one, and updates total coinns earned

        """
        self.current_level += 1
        self.total_coins += self.level.accumulated_coins

        self.level = Level(self.current_level, self.player)
        self.reset()

    def reset(self) -> None:
        """ Clears unneccesary objects when transitioning between levels (bullets, items, player position)

        """
        # Reset Bullets
        Bullet.set_index(0)
        Bullet.bullets = []

        # Reset player pos
        self.player.boxCollider = pygame.Rect(100, 100, 40, 85)

        # Reset items
        Item.items.clear()

    def save_coins(self) -> None:
        """ Opens json file, update and save total coins 

        """
        self.total_coins += self.level.accumulated_coins
        with open("game/data/store.json", "r") as f:
            data = json.load(f)
        data['coins'] += self.total_coins
        with open("game/data/store.json", "w") as f:
            json.dump(data, f, indent=4)

class Level():
    maps = [Map("map1.csv"), Map("map2.csv"),  Map("map3.csv")]

    def __init__(self, level: int, player: Character) -> None:
        self.player = player
        self.level = level
        self.map = Level.maps[level]
        self.collision_tiles, self.tiles = Level.maps[level].get_tile_map()
        self.accumulated_coins = 0

        self.gate = None

        # enemies
        self.enemies_list = []

        self.waves = 3
        self.done = False

        self.game_text = pygame.font.SysFont('Times New Roman', 75)
        self.text_opacity = 0

        # temp
        self.companion = Companion(100, 100)

    def update(self) -> None:
        """ Updates all entities in the game (player, enemy, bullet...)

        """
        self.player.animation.animate(
            self.player.run_frames if self.player.velocity else self.player.idle_frames)
        self.player.update(self.collision_tiles)

        for enemy in self.enemies_list:
            if not enemy.frozen:
                enemy.update(self.collision_tiles)

            if enemy.hp <= 0:
                from game.gamemanager import GameManager
                GameManager.progress[enemy._name] += 1
                self.enemies_list.remove(enemy)
                num = random.randrange(10)
                if num == 0:
                    ExtraHealth(enemy.rect.x, enemy.rect.y,
                                "game/sprites/items/hearts.png")
                elif num == 1:
                    Ammo(enemy.rect.x, enemy.rect.y,
                         "game/sprites/items/ammo.png")
                elif num == 2:
                    ExtraShield(enemy.rect.x, enemy.rect.y,
                                "game/sprites/items/shield.png")
                self.accumulated_coins += 20

        # temp
        self.companion.update(
            self.enemies_list, self.player, self.collision_tiles)

        for i in range(len(Bullet.bullets)):
            bullet = Bullet.bullets[i]
            if bullet:
                bullet.update(self.collision_tiles,
                              self.player, self.enemies_list)

        # enemy waves
        if len(self.enemies_list) == 0 and self.waves > 0:
            if self.level == 2 and self.waves == 1:
                self.enemies_list.append(Boss(400, 400, self.player))
            else:
                self.spawnEnemies()
            self.waves -= 1
            self.text_opacity = 255

        # boss ram dmg
        if self.level == 2 and self.waves == 0:
            if len(self.enemies_list) != 0 and self.player.boxCollider.colliderect(self.enemies_list[0]) and self.player.i_frames == 0:
                self.player.i_frames = 60
                self.player.set_hearts(-1)

        # spawn gate
        if self.waves == 0 and len(self.enemies_list) == 0:
            self.spawnGate()
            self.waves -= 1

        # items
        for item in Item.items:
            item.update(self.player)

        # gate
        if self.gate != None:
            if self.player.boxCollider.colliderect(self.gate):
                # Store Progress when you Enter the Gate
                with open("game/data/progress.json", "w") as f:
                    from game.gamemanager import GameManager
                    GameManager.progress["Level"] += 1
                    json.dump(GameManager.progress, f, indent=4)
                self.done = True

        if self.player.data["special"] == "kamziazie":
            self.player.special_attk.explode_damage(self.player.boxCollider, self.enemies_list)
        elif self.player.data["special"] == "freezing":
            self.player.special_attk.active_count(600)
            self.player.special_attk.passive_damage(self.enemies_list)
        elif self.player.data["special"] == "stealth":
            self.player.special_attk.active_count(300)

    def draw(self, surface: pygame.surface) -> None:
        """ Draws all entities onto screen

        Args: 
           surface: screen to blit onto

        """
        self.map.draw(surface)

        if self.gate:
            surface.blit(pygame.transform.scale(portal, [50, 100]), [
                         self.gate.x, self.gate.y - 25])
            # pygame.draw.rect(surface, (0, 255, 0), self.gate)

        # items
        for item in Item.items:
            item.draw(surface)

        for enemy in self.enemies_list:
            enemy.draw(surface)

            if self.player.special_attk.used == -1 and self.player.data["special"] == "freezing" and enemy.frozen:
                Animation.masking(enemy, surface)

        self.companion.draw(surface)
        self.player.draw(surface)

        for bullet in Bullet.bullets:
            if bullet:
                bullet.draw(surface)

        if self.text_opacity > 0:
            self.text_opacity -= 3

        level_text = self.game_text.render(
            f"{self.level + 1} - {3 - self.waves}", True, (255, 255, 255))
        text_rect = level_text.get_rect(center=(700, 270))
        level_text.set_alpha(self.text_opacity)
        surface.blit(level_text, text_rect)

    def spawnEnemies(self) -> None:
        """ Spawns random amount of enemies

        """
        total_enemy = random.randint(8, 12)

        sniper = random.randint(0, total_enemy // 3)
        total_enemy -= sniper
        for _ in range(sniper):
            tile = self.tiles[random.randrange(len(self.tiles) - 1)]
            self.enemies_list.append(SniperEnemy(tile.x, tile.y, self.player))

        shotgun = random.randint(1, total_enemy // 2)
        total_enemy -= shotgun
        for _ in range(shotgun):
            tile = self.tiles[random.randrange(len(self.tiles) - 1)]
            self.enemies_list.append(ShotgunEnemy(tile.x, tile.y, self.player))

        for _ in range(total_enemy):
            tile = self.tiles[random.randrange(len(self.tiles) - 1)]
            self.enemies_list.append(PistolEnemy(tile.x, tile.y, self.player))

    def spawnGate(self) -> None:
        """ Spawns a gate and random weapon at the end of each level

        """
        self.gate = self.tiles[random.randrange(len(self.tiles) - 1)]
        temp = self.tiles[random.randrange(len(self.tiles) - 1)]
        if self.level != 2:
            Chest(temp.x, temp.y, "game/sprites/chest.png")

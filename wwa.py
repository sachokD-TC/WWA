import pytmx
import pygame
from pytmx.util_pygame import load_pygame
from players.cowboy import Cowboy

WIN_WIDTH = 800
WIN_HEIGHT = 800

SCORE_POS_X = 520
SCORE_POS_Y = 750

LEVEL_POS_X = 250
LEVEL_POS_Y = 400

red = pygame.Color(153, 0, 0)


class Wwa():
    def __init__(self, level):
        pygame.init()
        self.rect = []
        self.level = level
        self.clock = pygame.time.Clock()
        self.cactus_count = 0
        self.life = 100
        self.game_display = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.pytmx_map = load_pygame("map//desert.tmx")
        self.score_image = pygame.image.load('pic/scores_brown.png')
        self.level_image = pygame.image.load('pic/level.png')
        self.pick_sound = pygame.mixer.Sound('sounds/pick.wav')
        self.hit_sound = pygame.mixer.Sound('sounds/hit.wav')
        self.over_sound = pygame.mixer.Sound('sounds/over.wav')
        self.main_loop()

    def step_back(self, block):
        block.rect.x -= block.movement_dict[block.movement][0]
        block.rect.y -= block.movement_dict[block.movement][1]
        block.pos_x += block.movement_dict[block.movement][0]
        block.pos_y += block.movement_dict[block.movement][1]

    def life_dec(self, life):
        font = pygame.font.SysFont("JOKERMAN", 25)
        text = font.render(str(life), True, (255, 255, 255))
        self.game_display.blit(text, (SCORE_POS_X + 220, SCORE_POS_Y + 5))

    def cactus_inc(self, cactus):
        font = pygame.font.SysFont("JOKERMAN", 25)
        text = font.render(str(cactus), True, (255, 255, 255))
        self.game_display.blit(text, (SCORE_POS_X + 80, SCORE_POS_Y + 5))

    def redraw_pics(self):
        for layer in self.pytmx_map.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x in range(0, 40):
                    for y in range(0, 40):
                        image = self.pytmx_map.get_tile_image(x, y, 0)
                        if image != None and (x, y) not in self.rect:
                            self.pics.blit(image, (32 * x, 32 * y))
                        else:
                            surface_image = pygame.image.load('map//tmw_desert_spacing.png')
                            self.pics.blit(surface_image, (32 * x, 32 * y), (5 * 32 + 6, 3 * 32 + 4, 32, 32))

    def show_level(self):
        self.game_display.fill(pygame.Color(244, 215, 65))
        pygame.display.update()
        self.game_display.blit(self.level_image, (LEVEL_POS_X, LEVEL_POS_Y))
        font = pygame.font.SysFont("JOKERMAN", 25)
        text = font.render('Level ' + str(self.level), True, (255, 255, 255))
        self.game_display.blit(text, (LEVEL_POS_X + 100, LEVEL_POS_Y + 5))
        pygame.display.update()
        pygame.time.delay(3000)

    def main_loop(self):
        self.block = Cowboy(pygame.Color(153, 0, 0), 32, 32)
        self.background = pygame.Surface((42 * 32, 42 * 32))
        self.pics = pygame.Surface((42 * 32, 42 * 32))
        self.loop = True
        self.event = None
        self.redraw_pics()
        self.show_level()

        while (self.loop):
            for event in pygame.event.get():
                pass
            layer_index = 0
            for layer in self.pytmx_map.visible_layers:
                layer_index += 1
                if isinstance(layer, pytmx.TiledObjectGroup):
                    if layer.name == 'pic_objs':
                        for obj in layer:
                            collision_rect = pygame.Rect(self.block.rect.x, self.block.rect.y, 32, 32)
                            if pygame.Rect(obj.x + self.block.pos_x, obj.y + self.block.pos_y, obj.width,
                                           obj.height).colliderect(collision_rect) == True:
                                cactus = (round(obj.x / 32), round(obj.y / 32))
                                if cactus not in self.rect:
                                    self.cactus_count += 1
                                    self.cactus_inc(self.cactus_count)
                                    self.rect.append(cactus)
                                    self.redraw_pics()
                                    self.pick_sound.play()
                                    break
                    if layer.name == "boxes":
                        for obj in layer:
                            collision_rect = pygame.Rect(self.block.rect.x, self.block.rect.y, 32, 32)
                            if pygame.Rect(obj.x + self.block.pos_x, obj.y + self.block.pos_y, obj.width,
                                           obj.height).colliderect(collision_rect) == True:
                                self.step_back(self.block)
                                self.life -= 1
                                self.life_dec(self.life)
                                self.hit_sound.play()
                                if self.life <= 0:
                                    self.over_sound.play()
                                    pygame.time.delay(3000)
                                    self.loop = False
                                break

            self.block.update(event)
            self.game_display.blit(self.pics, (self.block.pos_x, self.block.pos_y))
            self.game_display.blit(self.score_image, (SCORE_POS_X - 20, SCORE_POS_Y - 10))
            self.life_dec(self.life)
            self.cactus_inc(self.cactus_count)
            self.block.draw(self.game_display)
            self.clock.tick(60)
            pygame.display.update()

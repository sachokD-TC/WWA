import pytmx
import pygame
import random
from levels import levels_names
from pytmx.util_pygame import load_pygame
from players.cowboy import Cowboy

FONT_NAME = 'JOKERMAN'

BOXES = "boxes"

PIC_OBJS = 'pic_objs'

EXIT = 'exit'

TELEPORT_LEVEL = 'teleport'

WIN_WIDTH = 800
WIN_HEIGHT = 800

SCORE_POS_X = 520
SCORE_POS_Y = 750

LEVEL_POS_X = 250
LEVEL_POS_Y = 400

SCORE_COUNT_POS_X = SCORE_POS_X + 220
SCORE_AND_CACTUS_POS_Y = SCORE_POS_Y + 5
CACTUS_COUNT_POS_X = SCORE_POS_X + 80

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
        self.teleports = None
        self.pytmx_map = load_pygame("map//" + levels_names[level - 1] + ".tmx")
        self.score_image = pygame.image.load('pic/scores_brown.png')
        self.level_image = pygame.image.load('pic/level.png')
        self.pick_sound = pygame.mixer.Sound('sounds/pick.wav')
        self.hit_sound = pygame.mixer.Sound('sounds/hit.wav')
        self.over_sound = pygame.mixer.Sound('sounds/over.wav')
        self.finish_background = pygame.image.load('pic/level_completed.png')
        self.main_loop()

    def put_text(self, t, font_name, font_size, x, y, color):
        font = pygame.font.SysFont(font_name, font_size)
        text = font.render(str(t), True, color)
        self.game_display.blit(text, (x, y))

    def step_back(self, block):
        block.rect.x -= block.movement_dict[block.movement][0]
        block.rect.y -= block.movement_dict[block.movement][1]
        block.pos_x += block.movement_dict[block.movement][0]
        block.pos_y += block.movement_dict[block.movement][1]

    def redraw_pics(self):
        for layer in self.pytmx_map.visible_layers:
            if layer.name == TELEPORT_LEVEL:
                self.teleports = layer
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
        self.put_text('Level ' + str(self.level), 'JOKERMAN', 25, LEVEL_POS_X + 100, LEVEL_POS_Y + 5, (255, 255, 255))
        pygame.display.update()
        pygame.time.delay(3000)

    def show_final_scores(self):
        for i in range(0, self.cactus_count):
            self.put_text('Cactuses ' + str(i), 'JOKERMAN', 25, 190 + 100, 100 + 200, (0, 0, 0))
            pygame.display.update()
            pygame.time.delay(50)
            self.put_text('Cactuses ' + str(i), 'JOKERMAN', 25, 190 + 100, 100 + 200, (255, 255, 255))
            pygame.display.update()

    def show_finish(self):
        self.game_display.blit(self.finish_background, (190, 100))
        pygame.display.update()
        self.show_final_scores()
        pygame.time.delay(3000)
        self.level += 1
        Wwa(self.level)

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
                    if layer.name == TELEPORT_LEVEL:
                        for obj in layer:
                            collision_rect = pygame.Rect(self.block.rect.x, self.block.rect.y, 32, 32)
                            if pygame.Rect(obj.x + self.block.pos_x, obj.y + self.block.pos_y, obj.width,
                                           obj.height).colliderect(collision_rect) == True:
                                tnumber = random.randrange(0,len(self.teleports))
                                self.block.rect.x = self.teleports[tnumber].x
                                self.block.rect.y = self.teleports[tnumber].y
                                break
                    if layer.name == EXIT:
                        for obj in layer:
                            collision_rect = pygame.Rect(self.block.rect.x, self.block.rect.y, 32, 32)
                            if pygame.Rect(obj.x + self.block.pos_x, obj.y + self.block.pos_y, obj.width,
                                           obj.height).colliderect(collision_rect) == True:
                                self.show_finish()
                    if layer.name == PIC_OBJS:
                        for obj in layer:
                            collision_rect = pygame.Rect(self.block.rect.x, self.block.rect.y, 32, 32)
                            if pygame.Rect(obj.x + self.block.pos_x, obj.y + self.block.pos_y, obj.width,
                                           obj.height).colliderect(collision_rect) == True:
                                cactus = (round(obj.x / 32), round(obj.y / 32))
                                if cactus not in self.rect:
                                    self.cactus_count += 1
                                    self.put_text(self.cactus_count, FONT_NAME, 25, CACTUS_COUNT_POS_X,
                                                  SCORE_AND_CACTUS_POS_Y, (255, 255, 255))
                                    self.rect.append(cactus)
                                    self.redraw_pics()
                                    self.pick_sound.play()
                                    break
                    if layer.name == BOXES:
                        for obj in layer:
                            collision_rect = pygame.Rect(self.block.rect.x, self.block.rect.y, 32, 32)
                            if pygame.Rect(obj.x + self.block.pos_x, obj.y + self.block.pos_y, obj.width,
                                           obj.height).colliderect(collision_rect) == True:
                                self.step_back(self.block)
                                self.life -= 1
                                self.put_text(self.life, FONT_NAME, 25, SCORE_COUNT_POS_X, SCORE_AND_CACTUS_POS_Y,
                                              (255, 255, 255))
                                self.hit_sound.play()
                                if self.life <= 0:
                                    self.over_sound.play()
                                    pygame.time.delay(3000)
                                    self.loop = False
                                break

            self.block.update(event)
            self.game_display.blit(self.pics, (self.block.pos_x, self.block.pos_y))
            self.game_display.blit(self.score_image, (SCORE_POS_X - 20, SCORE_POS_Y - 10))
            self.put_text(self.life, FONT_NAME, 25, SCORE_COUNT_POS_X, SCORE_AND_CACTUS_POS_Y, (255, 255, 255))
            self.put_text(self.cactus_count, FONT_NAME, 25, CACTUS_COUNT_POS_X, SCORE_AND_CACTUS_POS_Y,
                          (255, 255, 255))
            self.block.draw(self.game_display)
            self.clock.tick(60)
            pygame.display.update()

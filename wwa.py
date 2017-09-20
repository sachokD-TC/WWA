import pytmx
import pygame
from levels import levels_names_times
from pytmx.util_pygame import load_pygame
from players.cowboy import Cowboy
from players.sun import Sun
from sound_play import Sound_play as sound


TIME_TAKEN_Y = 400

LAYER_DONE_PERCENT = 500

CACTUS_FINAL_Y = 300

FINAL_SCORES_X = 190 + 100

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

TIME_POS_X = 650
TIME_POS_Y = 5

TIME_INDEX=1
LEVEL_INDEX=0

red = pygame.Color(153, 0, 0)


class Wwa():
    def __init__(self, level, sound_on):
        pygame.init()
        self.time = levels_names_times[level-1][TIME_INDEX]
        self.rect = []
        self.level = level
        self.pic_obj_level = None
        self.clock = pygame.time.Clock()
        self.cactus_count = 0
        self.life = 100
        self.game_display = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.teleports = None
        self.pytmx_map = load_pygame("map//" + levels_names_times[level - 1][LEVEL_INDEX] + ".tmx")
        self.score_image = pygame.image.load('pic/scores_brown.png')
        self.level_image = pygame.image.load('pic/level.png')
        self.finish_background = pygame.image.load('pic/level_completed.png')
        self.sound = sound(sound_on)
        self.main_loop()

    def put_text(self, t, font_name, font_size, x, y, color):
        font = pygame.font.SysFont(font_name, font_size)
        text = font.render(str(t), True, color)
        self.game_display.blit(text, (x, y))

    def redraw_pics(self):
        for layer in self.pytmx_map.visible_layers:
            if layer.name == PIC_OBJS:
                self.pic_obj_level = layer
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
        self.put_text('Cactuses ' + str(self.cactus_count), 'JOKERMAN', 25, FINAL_SCORES_X, CACTUS_FINAL_Y, (0, 0, 0))
        time_taken = levels_names_times[self.level-1][TIME_INDEX] - self.time
        self.put_text('Time ' + str(time_taken), 'JOKERMAN', 25, FINAL_SCORES_X, TIME_TAKEN_Y, (0, 0, 0))
        percent_done =  (float)(self.cactus_count)/int(len(self.pic_obj_level))  * 100
        self.put_text('Layer done on ' + str(format(percent_done,'.2f')) + "%", 'JOKERMAN', 25, FINAL_SCORES_X, LAYER_DONE_PERCENT, (0, 0, 0))
        pygame.display.update()
        pygame.time.delay(50)


    def show_finish(self):
        self.game_display.blit(self.finish_background, (190, 100))
        pygame.display.update()
        self.show_final_scores()
        pygame.time.delay(3000)
        self.level += 1
        if self.level > len(levels_names_times):
            self.loop = False
        else:
            Wwa(self.level)

    def minus_life(self):
        self.life -= 1
        self.put_text(self.life, FONT_NAME, 25, SCORE_COUNT_POS_X, SCORE_AND_CACTUS_POS_Y,
                      (255, 255, 255))
        self.sound.play_hit_sound()
        if self.life <= 0:
            self.sound.play_game_over_sound()
            pygame.time.delay(3000)
            self.loop = False

    def main_loop(self):
        self.sun = Sun(250, 250, pygame.Rect(250, 350, 20, 120))
        self.cowboy = Cowboy(pygame.Color(153, 0, 0), 32, 32)
        self.background = pygame.Surface((42 * 32, 42 * 32))
        self.pics = pygame.Surface((42 * 32, 42 * 32))
        self.loop = True
        self.event = None
        self.redraw_pics()
        self.show_level()

        while (self.loop):
            self.time-=1;
            for event in pygame.event.get():
                pass
            layer_index = 0
            for layer in self.pytmx_map.visible_layers:
                layer_index += 1
                if isinstance(layer, pytmx.TiledObjectGroup):
                    if layer.name == EXIT:
                        for obj in layer:
                            collision_rect = pygame.Rect(self.cowboy.rect.x, self.cowboy.rect.y, 32, 32)
                            if pygame.Rect(obj.x + self.cowboy.pos_x, obj.y + self.cowboy.pos_y, obj.width,
                                           obj.height).colliderect(collision_rect) == True:
                                self.show_finish()
                    if layer.name == PIC_OBJS:
                        for obj in layer:
                            collision_rect = pygame.Rect(self.cowboy.rect.x, self.cowboy.rect.y, 32, 32)
                            if pygame.Rect(obj.x + self.cowboy.pos_x, obj.y + self.cowboy.pos_y, obj.width,
                                           obj.height).colliderect(collision_rect) == True:
                                cactus = (round(obj.x / 32), round(obj.y / 32))
                                if cactus not in self.rect:
                                    self.cactus_count += 1
                                    self.put_text(self.cactus_count, FONT_NAME, 25, CACTUS_COUNT_POS_X,
                                                  SCORE_AND_CACTUS_POS_Y, (255, 255, 255))
                                    self.rect.append(cactus)
                                    self.redraw_pics()
                                    self.sound.play_pick_sound()
                                    break
                    if layer.name == BOXES:
                        for obj in layer:
                            collision_rect = pygame.Rect(self.cowboy.rect.x, self.cowboy.rect.y, 32, 32)
                            if pygame.Rect(obj.x + self.cowboy.pos_x, obj.y + self.cowboy.pos_y, obj.width,
                                           obj.height).colliderect(collision_rect) == True:
                                self.cowboy.step_back()
                                self.minus_life()
                                break

            if self.cowboy.rect.colliderect(self.sun.rect):
                self.minus_life()

            self.cowboy.update(event)
            self.sun.update(-self.cowboy.movement_dict[self.cowboy.movement][0], -self.cowboy.movement_dict[self.cowboy.movement][1])
            self.game_display.blit(self.pics, (self.cowboy.pos_x, self.cowboy.pos_y))
            self.game_display.blit(self.score_image, (SCORE_POS_X - 20, SCORE_POS_Y - 10))
            self.put_text(self.life, FONT_NAME, 25, SCORE_COUNT_POS_X, SCORE_AND_CACTUS_POS_Y, (255, 255, 255))
            self.put_text(self.cactus_count, FONT_NAME, 25, CACTUS_COUNT_POS_X, SCORE_AND_CACTUS_POS_Y,
                          (255, 255, 255))
            self.put_text(self.time, FONT_NAME, 25, TIME_POS_X, TIME_POS_Y,
                          (255, 255, 255))
            self.sun.draw(self.game_display)
            self.cowboy.draw(self.game_display)
            self.clock.tick(60)
            pygame.display.update()

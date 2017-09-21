import pygame
import players.constants as const


class Cowboy(pygame.sprite.Sprite):
    def __init__(self, box):
        pygame.sprite.Sprite.__init__(self)
        self.box = box
        self.image = pygame.image.load('actors/right.png')
        self.rect = self.image.get_rect()
        self.is_step_back = False
        w = int(48)
        h = int(65)
        self.surface = pygame.Surface([w, h])
        self.actions = {const.LEFT: "left.png",
                        const.RIGHT: "right.png",
                        const.DOWN: "front.png",
                        const.UP: "back.png",
                        const.REST: "front.png"}
        self.action = "left"
        self.index = 200
        self.ind = 300
        self.rect.x = 50
        self.rect.y = 50
        self.pos_x = self.rect.x - 30
        self.pos_y = self.rect.y - 30
        self.movement_dict = {const.LEFT: (-2, 0), const.RIGHT: (2, 0), const.DOWN: (0, 2), const.UP: (0, -2), const.REST: (0, 0)}
        self.movement = 'rest'

    def update(self, event):
        if event != None:
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()
                elif event.key == pygame.K_LEFT:
                    self.movement = const.LEFT
                elif event.key == pygame.K_RIGHT:
                    self.movement = const.RIGHT
                elif event.key == pygame.K_DOWN:
                    self.movement = const.DOWN
                elif event.key == pygame.K_UP:
                    self.movement = const.UP
            elif event.type == pygame.KEYUP:
                self.movement = const.REST
        if self.rect.x < 15:
            self.rect.x = 15
            self.pos_x = 15
            self.is_step_back = True
        elif self.rect.y < 15:
            self.rect.y = 15
            self.pos_y = 15
            self.is_step_back = True
        if self.rect.y > 610:
            self.rect.y = 610
            self.pos_y = -610
            self.is_step_back = True
        if self.rect.x > 610:
            self.rect.x = 610
            self.pos_x = -610
            self.is_step_back = True
        else:
            self.rect.x += self.movement_dict[self.movement][0]
            self.rect.y += self.movement_dict[self.movement][1]
            self.pos_x -= self.movement_dict[self.movement][0]
            self.pos_y -= self.movement_dict[self.movement][1]
            self.image = pygame.image.load('actors/' + self.actions[self.movement])

    def draw(self, display):
        display.blit(self.image, self.rect)

    def step_back(self):
        self.rect.x -= self.movement_dict[self.movement][0]
        self.rect.y -= self.movement_dict[self.movement][1]
        self.pos_x += self.movement_dict[self.movement][0]
        self.pos_y += self.movement_dict[self.movement][1]

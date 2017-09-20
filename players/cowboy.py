import pygame
import players.constants as const

class Cowboy(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('actors/right.png')
        self.rect = self.image.get_rect()
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
        self.rect.x = 10
        self.rect.y = 10
        self.pos_x = self.rect.x
        self.pos_y = self.rect.y
        self.movement_dict = {'left': (-2, 0), 'right': (2, 0), 'down': (0, 2), 'up': (0, -2), 'rest': (0, 0)}
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
            self.pos_x =15
        elif self.rect.y < 15:
            self.rect.y = 15
            self.pos_y = 15
        if self.rect.y > 610:
            self.rect.y = 610
            self.pos_y = -610
        if self.rect.x > 610:
            self.rect.x = 610
            self.pos_x = -610
        else:
            self.rect.x += self.movement_dict[self.movement][0]
            self.rect.y += self.movement_dict[self.movement][1]
            self.pos_x -= self.movement_dict[self.movement][0]
            self.pos_y -= self.movement_dict[self.movement][1]
            self.image =  pygame.image.load('actors/' + self.actions[self.movement])

    def draw(self, display):
        display.blit(self.image, self.rect)


    def step_back(self):
        self.rect.x -= self.movement_dict[self.movement][0]
        self.rect.y -= self.movement_dict[self.movement][1]
        self.pos_x += self.movement_dict[self.movement][0]
        self.pos_y += self.movement_dict[self.movement][1]
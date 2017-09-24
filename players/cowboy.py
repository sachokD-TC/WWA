import pygame
import players.constants as const


class Cowboy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('actors/right.png')
        self.rect = self.image.get_rect()
        self.actions = {const.LEFT: ["left.png", "left_1.png", "left.png", "left_2.png"],
                        const.RIGHT: ["right.png", "right_1.png", "right.png", "right_2.png"],
                        const.DOWN: ["front.png", "front_1.png", "front.png", "front_2.png"],
                        const.UP: ["back.png", "back_1.png","back.png", "back_2.png"],
                        const.REST: ["front.png"]}
        self.action = "left"
        self.rect.x = 50
        self.rect.y = 50
        self.ind = 0
        self.move_in_row = 0;
        self.prev_move = const.REST
        self.pos_x = self.rect.x - 40
        self.pos_y = self.rect.y - 40
        self.movement_dict = {const.LEFT: (-2, 0), const.RIGHT: (2, 0), const.DOWN: (0, 2), const.UP: (0, -2),
                              const.REST: (0, 0)}
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
            self.inc_ind(self.movement)
            self.rect.x += self.movement_dict[self.movement][0]
            self.rect.y += self.movement_dict[self.movement][1]
            self.pos_x -= self.movement_dict[self.movement][0]
            self.pos_y -= self.movement_dict[self.movement][1]
            self.image = pygame.image.load('actors/' + self.actions[self.movement][self.ind])

    def inc_ind(self, move):
        if self.ind >= len(self.actions[move]) - 1:
            self.ind = 0
        else:
            self.ind += 1

    def draw(self, display):
        display.blit(self.image, self.rect)

    def step_back(self):
        self.is_step_back = True
        self.rect.x -= self.movement_dict[self.movement][0]
        self.rect.y -= self.movement_dict[self.movement][1]
        self.pos_x += self.movement_dict[self.movement][0]
        self.pos_y += self.movement_dict[self.movement][1]

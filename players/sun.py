import pygame
import players.constants as const


class Sun(pygame.sprite.Sprite):
    def __init__(self, box):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('actors/sun.png')
        self.rect = self.image.get_rect()
        self.rect.x = box.x
        self.rect.y = box.y
        self.box = box
        self.surface = pygame.Surface([32, 32])
        self.pos_x = self.rect.x
        self.pos_y = self.rect.y
        self.movement_dict = {const.LEFT: (-2, 0), const.RIGHT: (2, 0),const.UP: (0, -2),const.DOWN: (0, 2)}
        self.movements_order = [const.UP, const.RIGHT, const.DOWN, const.LEFT]
        self.movement = const.DOWN

    def update(self, delta_x, delta_y):
        self.rect.x += self.movement_dict[self.movement][0] + delta_x
        self.rect.y += self.movement_dict[self.movement][1] + delta_y
        self.box.x += delta_x
        self.box.y += delta_y
        self.check_box(self.box)

    def change_dir(self):
        next_ind = self.movements_order.index(self.movement) + 1
        if next_ind > len(self.movements_order) - 1:
            next_ind = 0
        self.movement = self.movements_order[next_ind]

    def check_box(self, box):
        if box.collidepoint((self.rect.x, self.rect.y)) == False:
            self.change_dir()

    def draw(self, display):
        display.blit(self.image, self.rect)

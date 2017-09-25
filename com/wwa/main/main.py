import pygame
import pytmx
from pytmx.util_pygame import load_pygame

from com.wwa.main.wwa import Wwa

MAP_MENU_BACKGROUND_TMX = "../map/menu_background.tmx"

PIC_MENU_PNG = '../pic/menu.png'

HATICON_PNG = '../pic/haticon.png'

pygame.init()

class GameMenu():
    def __init__(self, screen, items, bg_color=(0, 0, 0), font=None, font_size=70,
                 font_color=(15, 12, 0)):
        self.screen = screen
        self.back_img = pygame.Surface((42 * 32, 42 * 32))
        self.scr_width = self.screen.get_rect().width
        self.scr_height = self.screen.get_rect().height

        self.bg_color = bg_color
        self.clock = pygame.time.Clock()

        self.items = items
        self.font = pygame.font.SysFont(font, font_size)
        self.font_color = font_color
        self.menu_image = pygame.image.load(PIC_MENU_PNG)
        self.back_map = load_pygame(MAP_MENU_BACKGROUND_TMX)

        self.items = []
        for index, item in enumerate(items):
            label = self.font.render(item, 1, font_color)

            width = label.get_rect().width
            height = label.get_rect().height

            posx = (self.scr_width / 2) - (width / 2)
            t_h = len(items) * height
            posy = (self.scr_height / 2 ) - (t_h / 2) + (index * height)

            self.items.append([item, label, (width, height), (posx, posy)])

    def redraw_menu(self, new=None):
        for name, label, (width, height), (posx, posy) in self.items:
            if new is not None and new == name:
                new = self.font.render(name, 1, (255, 255, 0))
                self.screen.blit(new, (posx, posy + 45))
            else:
                self.screen.blit(label, (posx, posy + 45))


    def run(self):
        self.redraw_map()
        screen.blit(self.back_img, (0, 0))
        screen.blit(self.menu_image, (190, 100))
        self.redraw_menu()
        pygame.display.update()

        mainloop = True
        xmove = 0
        inc = -1
        while mainloop:
            self.clock.tick(50)
            posm =pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()
            new = None
            for name, label, (width, height), (posx, posy) in self.items:
                if posm[0] > posx and posm[0] < posx + width and posm[1] > posy and posm[1] < posy + height:
                    new = name
                    pygame.display.update()
                    if click[0] and name == 'Quit':
                        mainloop = False
                    if click[0] and name == 'Start':
                        Wwa(1, True, False)
                    if click[0] and name == 'About':
                        print('About - is clicked')

            screen.blit(self.back_img, (xmove, 0))
            if xmove <= -400:
                inc = 1
            if xmove > 0:
                inc =-1
            xmove += inc;

            screen.blit(self.menu_image, (190, 100))
            self.redraw_menu(new)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    mainloop = False

    def redraw_map(self):
        for layer in self.back_map.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x in range(0, 40):
                    for y in range(0, 40):
                      image = self.back_map.get_tile_image(x, y, 0)
                      if image != None:
                        self.back_img.blit(image, (32 * x, 32 * y))

if __name__ == "__main__":
    # Creating the screen
    screen = pygame.display.set_mode((800, 800), 0, 32)
    icon = pygame.image.load(HATICON_PNG)
    pygame.display.set_icon(icon)

    menu_items = ('Start', 'About', 'Quit')

    pygame.display.set_caption('Wild West Adventure')
    gm = GameMenu(screen, menu_items, (175,159,75),'JOKERMAN')
    gm.run()
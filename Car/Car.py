import random

import pygame as pg

pg.init()
screen_width = pg.display.get_desktop_sizes()[0][0]
screen_height = pg.display.get_desktop_sizes()[0][1]
# print(screen_width, screen_height)
screen_scale_y = 1536 / screen_width
screen_scale_x = 960 / screen_height
# print(screen_scale_x, screen_scale_y)
screen = pg.display.set_mode((screen_width, screen_height), pg.RESIZABLE)
clock = pg.time.Clock()

small_font = 30 * ((screen_scale_x + screen_scale_y) / 2)
seconds = 0
item_list = []
score1 = 0
score2 = 0


class Items:
    def __init__(self, height, width, colour):
        self.height = height
        self.width = width
        self.colour = colour
        self.x = random.randint(0, screen_width - self.width)
        self.y = random.randint(0, screen_height - self.height)
        self.rect = pg.Rect(self.x, self.y, self.width, self.height)

    def spawn(self, screen):
        pg.draw.rect(screen, self.colour, self.rect)

    def check_collision(self, ship):
        ship_rect = pg.Rect(ship.x, ship.y, ship.width, ship.height)
        if self.rect.colliderect(ship_rect):

            return True
        else:
            return False


class Ship:
    def __init__(self, x, y, width, height, up_key, down_key, left_key, right_key):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel_x = 20
        self.vel_y = 20
        self.up_key = up_key
        self.down_key = down_key
        self.left_key = left_key
        self.right_key = right_key

    def move(self):
        keys = pg.key.get_pressed()
        if keys[self.up_key] and self.y > 0:
            self.y -= self.vel_y
            if self.y < 0:
                self.y = 0
        if keys[self.down_key] and self.y + self.height < screen_height:
            self.y += self.vel_y
            if self.y > screen_height - self.height:
                self.y = screen_height - self.height
        if keys[self.left_key] and self.x > 0:
            self.x -= self.vel_x
            if self.x < 0:
                self.x = 0
        if keys[self.right_key] and self.x + self.width < screen_width:
            self.x += self.vel_x
            if self.x >= screen_width - self.width:
                self.x = screen_width - self.width

    def draw(self, screen):
        pg.draw.rect(screen, (255, 0, 0), (self.x, self.y, self.width, self.height))


font = pg.font.SysFont("comicsans", int(small_font))

ship = Ship(screen_width / 2, screen_height / 2, 100, 200, pg.K_w, pg.K_s, pg.K_a, pg.K_d)
running = True
while running:
    seconds += clock.tick(60) / 1000
    # print(seconds)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_BACKSPACE:
                running = False

    screen.fill((0, 0, 0))
    if seconds >= 0.1:
        for i in range(2):
            item_list.append(Items(20, 40, (100, 100, 100)))

        seconds = 0
    for item in item_list[:]:
        item.spawn(screen)
        if item.check_collision(ship):
            item_list.remove(item)
            score1 += 1

    ship.move()
    ship.draw(screen)
    score_left_text = font.render(str(score1), True, (255, 255, 255))
    screen.blit(score_left_text, (50 * screen_scale_x, 10 * screen_scale_y))
    # print(items_list)
    pg.display.flip()

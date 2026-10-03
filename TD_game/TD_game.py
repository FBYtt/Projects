import pygame as pg

pg.init()
screen_width = pg.display.get_desktop_sizes()[0][0]
screen_height = pg.display.get_desktop_sizes()[0][1]
print(screen_width, screen_height)
screen_scale_y = 1536 / screen_width
screen_scale_x = 960 / screen_height
# print(screen_scale_x, screen_scale_y)
screen = pg.display.set_mode((screen_width, screen_height), pg.RESIZABLE)
clock = pg.time.Clock()

minions = []
seconds = 0
lives = 3



class Monster:
    def __init__(self,health,width,height,speed,y):
        self.health = health
        self.width = width
        self.height = height
        self.colour = (255,0,0)
        self.speed = speed
        self.x = 200
        self.y = y
        self.rect = pg.Rect(self.x,self.y,self.width,self.height)
    def move(self):
        if self.y >= screen_height / 2 and self.x == 200:
            self.y -= self.speed
        if self.y <= screen_height / 2 and self.x <= screen_width - 200:
            self.x += self.speed
        if self.x >= screen_width - 200 - self.width and self.y < screen_height:
            self.y += self.speed




    def draw(self,screen):
        pg.draw.rect(screen, self.colour, (self.x, self.y, self.width, self.height))


running = True
paused = False
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_BACKSPACE:
                running = False
            if event.key == pg.K_ESCAPE:
                paused = not paused
            if event.key == pg.K_SPACE:
                minions.append(Monster(200,100,100,7,screen_height))
            if event.key == pg.K_DELETE:
                pass

    if not paused:
        screen.fill((50, 0, 0))
        seconds += clock.tick(60) / 1000
        if seconds >= 1:
            minions.append(Monster(200, 100, 100, 7, screen_height))
            seconds = 0
            print(len(minions))

        for minion in minions[:]:
            minion.move()
            minion.draw(screen)
            if minion.x >= screen_width - 200 - minion.width and minion.y >= screen_height:
                minions.remove(minion)
                lives -= 1




    pg.display.flip()

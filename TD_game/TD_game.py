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
bullets = []
seconds = 0
lives = 3
shoot_timer = 0



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
        if self.y >= screen_height / 3 and self.x == 200:
            self.y -= self.speed
        if self.y <= screen_height / 3 and self.x <= screen_width - 200:
            self.x += self.speed
        if self.x >= screen_width - 200 - self.width and self.y < screen_height:
            self.y += self.speed
    def draw(self,screen):
        pg.draw.rect(screen, self.colour, (self.x, self.y, self.width, self.height))


class Tower():
    def __init__(self,x,y,colour,shoot_speed):
        self.width = 50
        self.height = 50
        self.x = x
        self.y = y
        self.colour = colour
        self.shoot_speed = shoot_speed
    def draw(self,screen):
        pg.draw.rect(screen,self.colour, (self.x, self.y, self.width, self.height))


class Bullet:
    def __init__(self,x,y,vel_x,vel_y,damage,colour):
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.damage = damage
        self.colour = colour
        self.x = x
        self.y = y
        self.width = 5
        self.height = 5
        self.rect = pg.Rect(self.x,self.y,self.width,self.height)
    def move(self,minion):
        if self.y > minion.y + minion.height / 2:
            self.y -= self.vel_y
        if self.y < minion.y + minion.height / 2:
            self.y += self.vel_y
        if self.x > minion.x + minion.width / 2:
            self.x -= self.vel_x
        if self.x < minion.x + minion.width / 2:
            self.x += self.vel_x
    def draw(self,screen):
        pg.draw.circle(screen,self.colour, (self.x, self.y), self.width, self.height)
    def check_collision(self,minion):
        if self.rect.colliderect(minion.rect):
            minion.health -= self.damage
            return True
        else:
            return False


tower = Tower(screen_width/2,screen_height/1.2,(255,255,255),5)
bullet = Bullet(screen_width/2,screen_height/1.2,5,5,10,(0,0,0))
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
    tower.draw(screen)
    if not paused:
        seconds += clock.tick(60) / 1000
        shoot_timer += clock.tick(60) / 1000
        screen.fill((50, 0, 0))
        tower.draw(screen)

        if seconds >= 1:
            minions.append(Monster(200, 100, 100, 7, screen_height))
            seconds = 0
            print(len(minions))

        for minion in minions[:]:
            minion.move()
            minion.draw(screen)
            if minion.x >= screen_width - 200 - minion.width and minion.y >= screen_height:
                minions.remove(minion)

        if len(minions) > 0 and shoot_timer > 1:
            bullets.append(Bullet(tower.x,tower.y,15,15,10,(0,0,0)))
            shoot_timer = 0
        else:
            pass
        for bullet in bullets[:]:
            bullet.move(minions[0])
            bullet.draw(screen)
            if bullet.check_collision(minions[0]):
                bullets.remove(bullet)






    pg.display.flip()

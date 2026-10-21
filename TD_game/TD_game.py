import pygame as pg
import math
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
small_font = 20
#Fonts
font = pg.font.SysFont("comicsans", int(small_font))



class Monster:
    def __init__(self,health,width,height,speed,y):
        self.health = health
        self.width = width
        self.height = height
        self.colour = (35,35,35)
        self.speed = speed
        self.x = 200
        self.y = y
        self.rect = pg.Rect(self.x,self.y,self.width,self.height)
        self.state = 0
    def move(self):
        if self.y >= screen_height / 3 and self.x == 200:
            self.y -= self.speed
            self.state = 1
        if self.y <= screen_height / 3 and self.x <= screen_width - 200:
            self.x += self.speed
            self.state = 2
        if self.x >= screen_width - 200 - self.width and self.y < screen_height:
            self.y += self.speed
            self.state = 3
    def draw(self,screen):
        pg.draw.rect(screen, self.colour, (self.x, self.y, self.width, self.height))
        health = font.render(str(self.health), True, (255,255,255))
        screen.blit(health,(self.x + self.width /3,self.y + self.height))


class Tower():
    def __init__(self,x,y,colour,shoot_speed):
        self.width = 50
        self.height = 50
        self.x = x
        self.y = y
        self.colour = colour
        self.shoot_speed = shoot_speed
        self.timer = 0
    def calculate(self,minion):
        dx = (minion.x + minion.width/2) - (self.x+self.width/2)
        dy = (minion.y + minion.height/2) - (self.y+self.height/2)
        distance = math.hypot(dx,dy)
        return distance
    def draw(self,screen):
        pg.draw.rect(screen,self.colour, (self.x, self.y, self.width, self.height))
    def shoot(self,bullets):
        pass


class Bullet:
    def __init__(self,x,y,vel_x,vel_y,damage,colour):
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.damage = damage
        self.colour = colour
        self.x = x
        self.y = y
        self.width = 8
        self.height = 8
    def move(self,minion):
        if self.y > minion.y + minion.height / 2:
            self.y -= self.vel_y
        if self.y < minion.y + minion.height / 2:
            self.y += self.vel_y
        if self.x > minion.x + minion.width / 2:
            self.x -= self.vel_x
        if self.x < minion.x + minion.width / 2:
            self.x += self.vel_x
    def move_better(self,minion,tower):
        if minion.state == 1:
            pass
    def draw(self,screen):
        pg.draw.circle(screen,self.colour, (self.x, self.y), self.width, self.height)
    def check_collision(self,minion):
        minion.rect = pg.Rect(minion.x,minion.y,minion.width,minion.height)
        self.rect = pg.Rect(self.x,self.y,self.width,self.height)
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
        screen.fill((120, 120, 200))
        tower.draw(screen)

        if seconds >= 1:
            minions.append(Monster(10100, 100, 100, 3, screen_height))
            seconds = 0
            print(f"Nr of minions: {len(minions)}")

        for minion in minions[:]:
            minion.move()
            minion.draw(screen)
            if minion.x >= screen_width - 200 - minion.width and minion.y >= screen_height:
                minions.remove(minion)
            if minion.health <= 0:
                minions.remove(minion)

        if len(minions) > 0 and shoot_timer % 0.5 >= 0.485:
            bullets.append(Bullet(tower.x + tower.width/2,tower.y + tower.height/2,30,30,20,(140,0,0)))
            tower.calculate(minions[0])
        elif len(minions) <=0:
            del bullets[::]

        for bullet in bullets[:]:
            bullet.move(minions[0])
            bullet.draw(screen)
            if bullet.check_collision(minions[0]):
                bullets.remove(bullet)






    pg.display.flip()
